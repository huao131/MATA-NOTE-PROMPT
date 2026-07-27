"""Local drive mapping utilities for V1.1."""

from __future__ import annotations

from typing import Any


DEFAULT_MAPPING = {
    'EP003': {
        'series_folder_id': '1yrBvsVD46Y5q2xGxadWzSCxNLU2_YWLx',
        'episode_folder_id': '1RLx7C6BHUKWOo3uDU8qx8hvdBAkN4mUj',
        'folders': {
            '01_專案控制': '1L1W3h2nQZS7ztaA6-rV5BKI8okb5O_w6',
            '02_企劃與受眾洞察': '1C7-lbbaPHViFK6LvIeFtJFtXMgFlzhFr',
            '03_Hook與Creative': '1QOUooHiL_s4Wz28mZILqQbKKo09ceBJ8',
            '04_故事與腳本': '1uW-EzbW6VwigPzP5dDp80grlFJDjYea3',
            '05_Visual Bible': '1EGdWvL6TbzQ_HFSll4_evzXgjuipe2Rk',
            '06_Storyboard': '1NKknOClRNSftQTxhUNwiMh--Rueb_oA_',
            '07_Keyframes': '1X2GtTYjXioCT57w2yrGZkQhVOi9OxJek',
            '08_Flow Production': '1h12hf0ZiG7T103PpgoVYVfGPRwtWjIyl',
            '09_Audio': '1BcbfFzYDadTlc3fQTBOCAM50e7s-t6RB',
            '10_Subtitles': '1lEJxhrKvMkAOzWyTVsU0fKGrE7lmOPRm',
            '11_Editing Package': '1Iza8PYNgOB_kOkF8Q6Kj6s3Z8pDhbVGS',
            '12_Final Output': '1CpodaIgeZuoilY2ug3tf9SNNh7DBqBFZ',
            '13_Production Log': '1aNFRLj3druTLcYL7xLRRnPH3fWyqOBGy',
            '14_Rejected與Archive': '1J_LFQ5LV3AIpsCVdzSTNg7ERw2j6-i61',
        },
    }
}


def get_drive_mapping(episode_id: str) -> dict[str, Any]:
    if episode_id in DEFAULT_MAPPING:
        return {'status': 'LOCAL_CONFIGURATION', 'episode_id': episode_id, **DEFAULT_MAPPING[episode_id]}
    return {'status': 'DRIVE_NOT_CONNECTED', 'episode_id': episode_id, 'folders': {}}
