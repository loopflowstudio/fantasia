"""Exercise the deployed HTTPS assets and real WebSocket command path."""
from __future__ import annotations

import asyncio
import json
import sys
import urllib.request
from typing import Any

from websockets.asyncio.client import connect


async def verify(host: str) -> None:
    with urllib.request.urlopen(f'https://{host}/', timeout=30) as response:
        html = response.read().decode()
        assert response.status == 200 and '_app/immutable/' in html
    with urllib.request.urlopen(f'https://{host}/api/traces', timeout=30) as response:
        assert isinstance(json.load(response), list)
    async with connect(f'wss://{host}/ws/play', open_timeout=30) as socket:
        await socket.send(json.dumps({'type': 'new_game', 'config': {
            'hero_deck': {'Mountain': 12, 'Lightning Bolt': 12},
            'villain_deck': {'Island': 20}, 'villain_type': 'passive',
            'seed': 3, 'auto_pass': False,
        }}))
        # JSON from the public protocol; the assertions narrow expected messages.
        initial: dict[str, Any] = json.loads(await asyncio.wait_for(socket.recv(), 30))
        assert initial.get('type') != 'error', initial.get('message')
        frame = initial['recovery']['frame']
        assert frame['protocol'] == 1
        for action_type, label in (
            ('PRIORITY_PLAY_LAND', None),
            ('PRIORITY_CAST_SPELL', 'Cast Lightning Bolt'),
            ('CHOOSE_TARGET', 'Target Villain'),
            ('PRIORITY_PASS_PRIORITY', 'Pass priority'),
        ):
            offer = next(o for o in frame['offers'] if o['action_type'] == action_type and (label is None or o['label'] == label))
            command = {'command_id': f'cutover-{frame["revision"]}', 'match_id': frame['match_id'], 'expected_revision': frame['revision'], 'prompt_id': frame['prompt']['id'], 'offer_id': offer['id'], 'answers': []}
            await socket.send(json.dumps({'type': 'command', 'command': command}))
            outcome = json.loads(await asyncio.wait_for(socket.recv(), 30))
            assert outcome.get('status') == 'accepted', outcome.get('message', outcome.get('type'))
            frame = outcome['update']['frame']
        assert frame['projection']['opponent']['life'] == 17
        print(f'{host}: HTTPS SPA/API and four WebSocket commands passed; Lightning Bolt resolved for 3 damage')
    async with connect(f'wss://{host}/ws/play', open_timeout=30) as socket:
        await socket.send(json.dumps({'type': 'new_game', 'config': {'hero_deck_name': 'ur_lessons', 'villain_deck_name': 'gw_allies', 'villain_type': 'random', 'seed': 285}}))
        initial = json.loads(await asyncio.wait_for(socket.recv(), 30))
        assert initial.get('type') != 'error', initial.get('message')
        frame = initial['recovery']['frame']
        assert frame['offers'] and frame['asset_pack']
        print(f'{host}: curated Lessons versus Allies opened with legal offers and asset-pack identity')


if __name__ == '__main__':
    asyncio.run(verify(sys.argv[1]))
