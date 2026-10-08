import time
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.models.schemas import (
    UserContext, Challenge, GenerateChallengeRequest,
    ReflectionRequest, RewardResult, JourneyCard, SocialPost
)
from backend.app.services.memory_service import memory_service
from backend.app.services.reward_service import reward_service, ALL_BADGES
from backend.app.services.voice_service import voice_service
from backend.app.services.sentry_service import sentry_tracer
from backend.app.agent.gemma_orchestrator import gemma_orchestrator
from backend.app.agent.reflection_eval import reflection_evaluator
from backend.app.agent.policy_engine import policy_engine
from backend.app.services.tabpfn_service import tabpfn_service

app = FastAPI(
    title="TouchGrass API",
    description="Local-First, Open-AI Agent platform that gets people off screens and into the world.",
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "offline_mode": settings.OFFLINE_MODE,
        "ai_model": settings.GEMMA_MODEL,
        "memory_store": "MongoDB Atlas" if memory_service.db is not None else "Local-First JSON"
    }

@app.get("/api/user", response_model=UserContext)
async def get_user(user_id: str = "guest_user"):
    return memory_service.get_user_context(user_id)

@app.post("/api/user/toggle-offline")
async def toggle_offline(user_id: str = "guest_user"):
    user = memory_service.get_user_context(user_id)
    user.offline_mode = not user.offline_mode
    settings.OFFLINE_MODE = user.offline_mode
    memory_service.save_user_context(user)
    return {
        "offline_mode": user.offline_mode,
        "message": "Airplane / Local Trail mode enabled" if user.offline_mode else "Online Cloud Sync enabled"
    }

@app.get("/api/forecast/vitality")
async def get_vitality_forecast(
    hour: float = Query(default=10.5, ge=0.0, le=24.0),
    duration: int = Query(default=15, ge=5, le=120),
    focus: str = Query(default="Nature")
):
    """Predicts optimal outdoor presence window and vitality score using TabPFN"""
    start_time = time.time()
    result = tabpfn_service.predict_vitality_window(
        current_hour=hour,
        target_minutes=duration,
        user_preference=focus
    )
    sentry_tracer.trace_agent_execution(
        step_name="tabpfn.predict_vitality",
        duration_ms=(time.time() - start_time) * 1000,
        metadata={
            "vitality_score": result.get("vitality_score"),
            "optimal_window": result.get("optimal_window"),
            "focus": focus,
            "duration": duration
        }
    )
    return result

@app.post("/api/challenge/generate", response_model=Challenge)
async def generate_challenge(req: GenerateChallengeRequest):
    start_time = time.time()
    user = memory_service.get_user_context(req.user_id)
    recent_categories = memory_service.get_recent_categories(req.user_id)

    # 1. Gemma Agent generation with policy engine validation
    challenge = await gemma_orchestrator.generate_challenge(
        user=user,
        desired_category=req.desired_category,
        difficulty=req.difficulty,
        time_available=req.time_available_minutes or 20,
        recent_categories=recent_categories
    )

    # 2. Persist in memory store
    memory_service.record_challenge(challenge)

    # 3. Trace in Sentry
    duration_ms = (time.time() - start_time) * 1000
    sentry_tracer.trace_agent_execution(
        step_name="gemma.generate_challenge",
        duration_ms=duration_ms,
        metadata={
            "user_level": user.level,
            "category": challenge.category.value,
            "difficulty": challenge.difficulty.value,
            "offline_mode": user.offline_mode
        }
    )

    return challenge

@app.get("/api/voice/speak")
async def speak_text(text: str):
    """Voice layer using ElevenLabs with offline Web Speech fallback"""
    return await voice_service.generate_speech(text)

@app.post("/api/challenge/reflect", response_model=RewardResult)
async def submit_reflection(req: ReflectionRequest, user_id: str = "guest_user"):
    start_time = time.time()
    user = memory_service.get_user_context(user_id)
    challenge = memory_service.get_challenge(req.challenge_id)

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # 1. Gemma Evaluator analyzes reflection & effort
    bonus_xp, encouragement, sincerity = reflection_evaluator.evaluate(
        reflection_text=req.reflection_text,
        minutes_spent=req.minutes_spent
    )

    # 2. Reward Engine computes XP, Level progression, Badges, Unlocks
    reward = reward_service.evaluate_reward(
        user=user,
        challenge=challenge,
        bonus_xp=bonus_xp,
        encouragement=encouragement,
        sincerity_score=sincerity
    )

    # 3. Save to long-term memory
    memory_service.save_user_context(user)
    memory_service.record_completion(
        user_id=user_id,
        challenge=challenge,
        reflection=req.reflection_text,
        minutes=req.minutes_spent,
        reward=reward
    )

    # 4. Trace in Sentry
    duration_ms = (time.time() - start_time) * 1000
    sentry_tracer.trace_agent_execution(
        step_name="gemma.evaluate_reflection",
        duration_ms=duration_ms,
        metadata={
            "total_xp_awarded": reward.total_xp_awarded,
            "level_up": reward.level_up,
            "new_level": reward.new_level,
            "sincerity_score": sincerity
        }
    )

    return reward

@app.get("/api/social/feed")
async def get_social_feed(user_id: str = "guest_user"):
    user = memory_service.get_user_context(user_id)
    feed = memory_service.get_social_feed()
    return {
        "unlocked": user.level >= 5 or "social_mode" in user.unlocked_features,
        "required_level": 5,
        "current_level": user.level,
        "feed": feed
    }

@app.get("/api/journey", response_model=JourneyCard)
async def get_journey_card(user_id: str = "guest_user"):
    user = memory_service.get_user_context(user_id)
    completions = memory_service.get_all_completions(user_id)

    cat_counts = {}
    quotes = []
    for c in completions:
        cat = c.get("category", "Outdoor")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        ref = c.get("reflection", "")
        if ref and len(ref) > 15 and len(quotes) < 3:
            quotes.append(f'"{ref}"')

    if not quotes:
        quotes = [
            '"Took a 20-minute walk with zero screens."',
            '"Helped someone smile in the real world."',
            '"Noticed the colors of the horizon."'
        ]

    badges_data = [
        {"id": b, "title": ALL_BADGES.get(b, {}).get("title", b), "icon": ALL_BADGES.get(b, {}).get("icon", "🏅")}
        for b in user.badges
    ]

    summary = (
        f"TouchGrass Journey: Level {user.level} | "
        f"{user.completed_challenges_count} real-world outdoor missions completed. "
        f"Real life > Screen time."
    )

    return JourneyCard(
        username=user.username,
        level=user.level,
        total_challenges=user.completed_challenges_count,
        categories_breakdown=cat_counts if cat_counts else {"Outdoor": 1, "Nature": 1},
        badges_earned=badges_data,
        notable_quotes=quotes,
        shareable_summary=summary
    )

@app.get("/api/observability/traces")
async def get_traces():
    return sentry_tracer.get_recent_traces()

# Video walkthrough studio & audio files
audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../audio"))
if os.path.exists(audio_dir):
    app.mount("/audio", StaticFiles(directory=audio_dir), name="audio")

video_html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../video_walkthrough.html"))
@app.get("/demo-video")
async def serve_demo_video():
    if os.path.exists(video_html_path):
        return FileResponse(video_html_path)
    raise HTTPException(status_code=404, detail="Demo video studio not found")

# Mount frontend/dist if built
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/dist"))
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        index_file = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Frontend build not found"}

