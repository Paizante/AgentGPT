"""Testes do modo 'criar, nunca destruir': copia segura, backup antes de
sobrescrever e listagem de arquivos."""
from __future__ import annotations

from src import file_utils


def test_garantir_pasta_cria_pastas_aninhadas(tmp_path):
    destino = tmp_path / "a" / "b" / "c"
    resultado = file_utils.garantir_pasta(destino)
    assert resultado.exists()
    assert resultado.is_dir()


def test_copiar_arquivo_seguro_nao_apaga_original(tmp_path):
    origem = tmp_path / "original.txt"
    origem.write_text("conteudo original", encoding="utf-8")
    destino = tmp_path / "saida" / "copia.txt"

    resultado = file_utils.copiar_arquivo_seguro(origem, destino)

    assert origem.exists()
    assert origem.read_text(encoding="utf-8") == "conteudo original"
    assert resultado.read_text(encoding="utf-8") == "conteudo original"


def test_copiar_arquivo_seguro_faz_backup_antes_de_sobrescrever(workspace, tmp_path):
    origem_v1 = tmp_path / "v1.txt"
    origem_v1.write_text("versao 1", encoding="utf-8")
    origem_v2 = tmp_path / "v2.txt"
    origem_v2.write_text("versao 2", encoding="utf-8")
    destino = tmp_path / "saida" / "documento.txt"

    file_utils.copiar_arquivo_seguro(origem_v1, destino)
    file_utils.copiar_arquivo_seguro(origem_v2, destino)

    assert destino.read_text(encoding="utf-8") == "versao 2"
    backups_dir = workspace / "10_BACKUPS" / "documentos" / "pre_sobrescrita"
    assert backups_dir.exists()
    arquivos_backup = list(backups_dir.iterdir())
    assert len(arquivos_backup) == 1
    assert arquivos_backup[0].read_text(encoding="utf-8") == "versao 1"


def test_listar_arquivos_filtra_por_extensao(tmp_path):
    (tmp_path / "doc.pdf").write_text("pdf", encoding="utf-8")
    (tmp_path / "doc.docx").write_text("docx", encoding="utf-8")
    (tmp_path / "doc.txt").write_text("txt", encoding="utf-8")

    arquivos_pdf = file_utils.listar_arquivos(tmp_path, extensoes=["pdf"])

    assert [a.name for a in arquivos_pdf] == ["doc.pdf"]


def test_listar_arquivos_pasta_inexistente_retorna_vazio(tmp_path):
    assert file_utils.listar_arquivos(tmp_path / "nao_existe") == []
