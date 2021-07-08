"""Combine multiple JSONs into one."""

import dataclasses
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from omegaconf.dictconfig import DictConfig

from pp.config import CONFIG, TECH, logger, write_config


def merge_json(
    doe_directory: Path = CONFIG["doe_directory"],
    gds_directory: Path = CONFIG["gds_directory"],
    extra_directories: Optional[Iterable[Path]] = None,
    jsonpath: Path = CONFIG["mask_directory"] / "metadata.json",
    json_version: int = 6,
    config: DictConfig = TECH,
) -> Dict[str, Any]:
    """Combine several JSON files from config.yml
    in the root of the mask directory, gets mask_name from there

    Args:
        doe_directory: defaults to current working directory
        extra_directories: list of extra_directories
        jsonpath
        json_version:
        config

    """
    logger.debug("Merging JSON files:")
    cells = {}
    extra_directories = extra_directories or []
    config = dataclasses.asdict(config)
    config.pop("library", "")

    for directory in extra_directories + [doe_directory]:
        for filename in directory.glob("*/*.json"):
            logger.debug(filename)
            with open(filename, "r") as f:
                data = json.load(f)
                cells.update(data.get("cells"))

    does = {d.stem: json.loads(open(d).read()) for d in doe_directory.glob("*.json")}
    metadata = dict(
        json_version=json_version,
        cells=cells,
        does=does,
        config=config,
    )

    write_config(metadata, jsonpath)
    logger.info(f"Wrote  metadata in {jsonpath}")
    return metadata


if __name__ == "__main__":
    from pprint import pprint

    d = merge_json()
    pprint(d)

    # print(config["module_versions"])
    # pprint(d['does'])

    # with open(jsonpath, "w") as f:
    #     f.write(json.dumps(d, indent=2))
