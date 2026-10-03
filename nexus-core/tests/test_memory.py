from pathlib import Path

from app.memory.manager import MemoryManager
from app.memory.models import MemoryCategory


def test_memory_store_and_search(tmp_path: Path):
    storage_file = tmp_path / "memory.json"
    mgr = MemoryManager(storage_file)

    mgr.remember("favorite_theme", "Cyberpunk dark mode with cyan accents", MemoryCategory.PREFERENCE)
    mgr.remember("project_goal", "Nexus AI local assistant and desktop client", MemoryCategory.SEMANTIC)

    recalled = mgr.recall("cyberpunk")
    assert len(recalled) == 1
    assert recalled[0].key == "favorite_theme"

    recalled_semantic = mgr.recall("Nexus", category=MemoryCategory.SEMANTIC)
    assert len(recalled_semantic) == 1
    assert recalled_semantic[0].key == "project_goal"

    # Test persistence
    mgr2 = MemoryManager(storage_file)
    assert mgr2.store.count() == 2
    assert len(mgr2.recall("cyberpunk")) == 1


def test_conversation_history_and_context_prompt():
    mgr = MemoryManager()
    mgr.remember("guideline", "Always maintain high coding standards", MemoryCategory.SEMANTIC)

    session_id = "test-session-1"
    mgr.add_message(session_id, "user", "Hello Nexus")
    mgr.add_message(session_id, "assistant", "Hello! How can I assist you today?")

    messages = mgr.get_messages(session_id)
    assert len(messages) == 2
    assert messages[0].content == "Hello Nexus"

    prompt = mgr.build_context_prompt("standards", session_id)
    assert "guideline" in prompt
    assert "Hello Nexus" in prompt
