"""校验独立插件索引并构建 MoviePilot 可安装的源码发布包。"""

import argparse
import ast
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ID = "CureTMDbAnimeShy"
PLUGIN_DIR = ROOT / "plugins.v3" / PLUGIN_ID.lower()


def build_release(output_dir: Path) -> Path:
    """确保索引与源码版本一致，并仅打包插件源码。"""
    index = json.loads((ROOT / "package.v3.json").read_text(encoding="utf-8"))
    if set(index) != {PLUGIN_ID}:
        raise ValueError("独立仓库索引必须只包含 CureTMDbAnimeShy")
    tree = ast.parse((PLUGIN_DIR / "__init__.py").read_text(encoding="utf-8"))
    plugin = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == PLUGIN_ID)
    version = next(
        ast.literal_eval(node.value)
        for node in plugin.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "plugin_version" for target in node.targets)
    )
    if index[PLUGIN_ID]["version"] != version:
        raise ValueError("插件源码版本与索引版本不一致")
    sources = sorted(PLUGIN_DIR.glob("*.py"))
    if not sources or not (PLUGIN_DIR / "__init__.py").is_file():
        raise ValueError("插件源码不完整")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{PLUGIN_ID.lower()}_v{version}.zip"
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for source in sources:
            archive.write(source, source.relative_to(PLUGIN_DIR).as_posix())
    return destination


def main() -> None:
    """从命令行指定输出目录，打印实际构建的安装包路径。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    print(build_release(args.output_dir))


if __name__ == "__main__":
    main()
