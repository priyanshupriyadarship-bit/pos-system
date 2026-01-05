#!/usr/bin/env python3
"""Test script to verify POS setup."""

import sys

print("=" * 60)
print("PRESENT OPERATING SYSTEM - SETUP TEST")
print("=" * 60)

# Test 1: Check imports
print("\n[TEST 1] Checking imports...")
try:
    from config.settings import Config
    print("✓ Config imported successfully")
except Exception as e:
    print(f"✗ Failed to import config: {e}")
    sys.exit(1)

try:
    from backend.core.llm_engine import LLMEngine
    print("✓ LLM Engine imported successfully")
except Exception as e:
    print(f"✗ Failed to import LLM Engine: {e}")
    sys.exit(1)

try:
    from backend.core.avatar_system import AvatarSystem, Avatar
    print("✓ Avatar System imported successfully")
except Exception as e:
    print(f"✗ Failed to import Avatar System: {e}")
    sys.exit(1)

# Test 2: Check configuration
print("\n[TEST 2] Checking configuration...")
print(f"✓ LLM Provider: {Config.LLM_PROVIDER}")
print(f"✓ Debug Mode: {Config.DEBUG}")
print(f"✓ Timezone: {Config.TIMEZONE}")

# Test 3: Create sample avatar
print("\n[TEST 3] Testing Avatar System...")
avatars = AvatarSystem("test_user")
print(f"✓ Created {len(avatars.avatars)} default avatars")
avatars.award_xp("Warrior", 50)
stats = avatars.get_stats()
print(f"✓ Total XP: {stats['total_xp']}")
print(f"✓ Balance: Warrior={stats['balance']['Warrior']:.1f}%")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
