import asyncio
from httpx import AsyncClient, ASGITransport
from backend.app.main import app

async def test_suite():
    print("=== STARTING TOUCHGRASS VERIFICATION SUITE ===")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health check
        res = await client.get("/api/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        print("✓ Health Check Passed:", res.json())

        # 2. Get User
        res = await client.get("/api/user")
        assert res.status_code == 200, f"User check failed: {res.text}"
        user_data = res.json()
        print(f"✓ User Context: Level {user_data['level']} | {user_data['xp']} XP | {len(user_data['badges'])} Badges")

        # 3. Generate Challenge with Gemma Agent
        res = await client.post("/api/challenge/generate", json={"user_id": "guest_user", "time_available_minutes": 20})
        assert res.status_code == 200, f"Generate challenge failed: {res.text}"
        ch = res.json()
        print(f"✓ Gemma Challenge Generated: '{ch['title']}' ({ch['category']}) | +{ch['xp_reward']} XP")
        print(f"  Spoken Audio Intro: '{ch['spoken_intro']}'")

        # 4. Submit Reflection (Simulating real-world action completed)
        reflection = "I stepped outside and helped my elderly neighbor carry groceries to her porch. We had a lovely 5-minute conversation."
        res = await client.post("/api/challenge/reflect", json={
            "challenge_id": ch["id"],
            "reflection_text": reflection,
            "minutes_spent": 20
        })
        assert res.status_code == 200, f"Reflect failed: {res.text}"
        reward = res.json()
        print(f"✓ Gemma Evaluator & Reward Engine: +{reward['total_xp_awarded']} Total XP (Base: {reward['base_xp']}, Bonus: {reward['bonus_xp']})")
        print(f"  Gemma Encouragement: '{reward['gemma_encouragement']}'")
        if reward['new_badges']:
            print(f"  🏅 Unlocked Badges: {reward['new_badges']}")

        # 5. Journey Card check
        res = await client.get("/api/journey")
        assert res.status_code == 200, f"Journey check failed: {res.text}"
        journey = res.json()
        print(f"✓ Journey Card: {journey['total_challenges']} completed | Badges: {len(journey['badges_earned'])}")

        # 6. Social Feed check
        res = await client.get("/api/social/feed")
        assert res.status_code == 200, f"Social feed failed: {res.text}"
        social = res.json()
        print(f"✓ Social Feed: Unlocked: {social['unlocked']} | {len(social['feed'])} Community Posts")

        # 7. Sentry Agent Traces
        res = await client.get("/api/observability/traces")
        assert res.status_code == 200, f"Traces failed: {res.text}"
        traces = res.json()
        print(f"✓ Sentry Agent Traces Recorded: {len(traces)} execution spans")
        for t in traces[-3:]:
            print(f"  - [{t['step']}] {t['duration_ms']}ms")

        # 8. Offline Airplane Mode Toggle Test
        res = await client.post("/api/user/toggle-offline")
        assert res.status_code == 200
        print(f"✓ Offline Toggle Test: {res.json()['message']}")

    print("=== ALL 8 TOUCHGRASS VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    asyncio.run(test_suite())
