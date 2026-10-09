"""Concurrent access must not corrupt the file backend."""
import asyncio
from lib.store import index_certificate, get_latest


def test_100_concurrent_writes(temp_store):
    async def write(i):
        await index_certificate(f"test/repo{i}", {
            "score": i % 100, "repo": f"test/repo{i}", "tier": "Gold"
        })

    async def main():
        await asyncio.gather(*[write(i) for i in range(100)])

    asyncio.run(main())

    async def check():
        count = 0
        for i in range(100):
            e = await get_latest(f"test/repo{i}")
            if e:
                count += 1
        return count

    assert asyncio.run(check()) == 100


def test_concurrent_read_write(temp_store):
    async def main():
        async def writer(i):
            await index_certificate(f"test/concurrent{i}", {"score": 50, "repo": f"test/concurrent{i}"})
        async def reader(i):
            await get_latest(f"test/concurrent{i}")
        await asyncio.gather(*[writer(i) for i in range(50)], *[reader(i) for i in range(50)])
    asyncio.run(main())
