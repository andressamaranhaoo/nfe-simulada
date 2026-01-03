import io
import re
import requests
import pandas as pd
import streamlit as st

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="NF-e Simulada", layout="centered")

st.title("NF-e Simulada")
st.caption("Interface do cliente (sem precisar mexer com JSON)")

API_URL = st.text_input("URL da API (FastAPI)", "http://127.0.0.1:8000").rstrip("/")

def get_json(path: str):
    r = requests.get(f"{API_URL}{path}", timeout=15)
    r.raise_for_status()
    return r.json()

def post_json(path: str, payload: dict | None = None):
    r = requests.post(f"{API_URL}{path}", json=payload, timeout=15)
    r.raise_for_status()
    return r.json()

def limpar_cnpj(cnpj: str) -> str:
    return re.sub(r"\D", "", (cnpj or "").strip())

def cnpj_valido_basico(cnpj: str) -> bool:
    cnpj = limpar_cnpj(cnpj)
    return len(cnpj) == 14 and cnpj.isdigit()

def normalize_lista_nfe(data):
    """
    Aceita lista de dicts (ideal) ou dict com chave 'items'/'data'/'results'.
    """
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ["items", "data", "results"]:
            if k in data and isinstance(data[k], list):
                return data[k]
    return []

def gerar_excel_bytes(registros: list[dict]) -> bytes:
    df = pd.DataFrame(registros)

    cols_pref = [
        "id_notafiscal", "empresa_nome", "empresa_cnpj",
        "emitente_nome", "destinatario_nome", "valor_total", "status", "chave"
    ]
    cols = [c for c in cols_pref if c in df.columns] + [c for c in df.columns if c not in cols_pref]
    if len(df.columns):
        df = df[cols]

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="NFs")
    return out.getvalue()

def gerar_pdf_bytes(registros: list[dict]) -> bytes:
    out = io.BytesIO()
    c = canvas.Canvas(out, pagesize=A4)
    w, h = A4

    y = h - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Relatório de NF-e (Simulada)")
    y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Total de registros: {len(registros)}")
    y -= 20

    # Cabeçalho
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, y, "ID NF")
    c.drawString(110, y, "Empresa")
    c.drawString(300, y, "CNPJ")
    c.drawString(380, y, "Destinatário")
    c.drawRightString(555, y, "Valor (R$)")
    y -= 14

    c.setFont("Helvetica", 9)

    for r in registros:
        if y < 50:
            c.showPage()
            y = h - 40
            c.setFont("Helvetica", 9)

        id_nf = str(r.get("id_notafiscal", ""))[:12]
        empresa = str(r.get("empresa_nome", ""))[:28]
        cnpj = str(r.get("empresa_cnpj", ""))[:14]
        dest = str(r.get("destinatario_nome", r.get("destinatario", "")))[:22]
        valor = r.get("valor_total", "")

        try:
            valor_fmt = f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            valor_fmt = str(valor)

        c.drawString(40, y, id_nf)
        c.drawString(110, y, empresa)
        c.drawString(300, y, cnpj)
        c.drawString(380, y, dest)
        c.drawRightString(555, y, valor_fmt)
        y -= 12

    c.showPage()
    c.save()
    return out.getvalue()

st.divider()

# Tabs: Criar / Consultar / Cancelar / Relatórios
tab1, tab2, tab3, tab4 = st.tabs(["➕ Criar", "🔍 Consultar", "🧨 Cancelar", "📑 Relatórios"])

# =========================
# 1) CRIAR
# =========================
with tab1:
    st.subheader("Criar NF")

    with st.form("form_criar"):
        colA, colB = st.columns(2)
        with colA:
            id_notafiscal = st.text_input("ID Nota Fiscal (identificador)")
            empresa_nome = st.text_input("Nome da empresa")
        with colB:
            empresa_cnpj = st.text_input("CNPJ da empresa")
            emitente_nome = st.text_input("Quem está emitindo (nome)")

        destinatario_nome = st.text_input("Quem vai receber (destinatário)")
        valor_total = st.number_input("Valor total (R$)", min_value=0.0, step=1.0)

        submitted = st.form_submit_button("Emitir NF ✅")

    if submitted:
        if empresa_cnpj and not cnpj_valido_basico(empresa_cnpj):
            st.error("CNPJ inválido (precisa ter 14 dígitos).")
        else:
            try:
                payload = {
                    "id_notafiscal": id_notafiscal,
                    "empresa_nome": empresa_nome,
                    "empresa_cnpj": limpar_cnpj(empresa_cnpj),
                    "emitente_nome": emitente_nome,
                    "destinatario_nome": destinatario_nome,
                    "valor_total": float(valor_total),
                }
                resp = post_json("/nfe/", payload)
                st.success("NF criada com sucesso!")
                st.json(resp)
            except Exception as e:
                st.error(f"Falhou: {e}")

# =========================
# 2) CONSULTAR
# =========================
with tab2:
    st.subheader("Consultar NF por chave/ID")
    chave = st.text_input("Chave (ou ID)")

    if st.button("Consultar 🔍"):
        try:
            st.json(get_json(f"/nfe/{chave}"))
        except Exception as e:
            st.error(f"Falhou: {e}")

# =========================
# 3) CANCELAR
# =========================
with tab3:
    st.subheader("Cancelar NF")
    chave_cancelar = st.text_input("Chave/ID para cancelar")

    if st.button("Cancelar 🧨"):
        try:
            st.json(post_json(f"/nfe/{chave_cancelar}/cancelar"))
            st.success("NF cancelada com sucesso!")
        except Exception as e:
            st.error(f"Falhou: {e}")

# =========================
# 4) RELATÓRIOS
# =========================
with tab4:
    st.subheader("Relatórios e exportação")

    if st.button("📃 Carregar lista de NFs"):
        try:
            data = get_json("/nfe/")
            regs = normalize_lista_nfe(data)

            if not regs:
                st.warning("Nenhum registro retornado pela API.")
            else:
                st.success(f"{len(regs)} NFs carregadas.")
                st.dataframe(pd.DataFrame(regs), use_container_width=True)

                xlsx_bytes = gerar_excel_bytes(regs)
                pdf_bytes = gerar_pdf_bytes(regs)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "⬇️ Baixar planilha (Excel)",
                        data=xlsx_bytes,
                        file_name="lista_nfe.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                with col2:
                    st.download_button(
                        "⬇️ Baixar relatório (PDF)",
                        data=pdf_bytes,
                        file_name="lista_nfe.pdf",
                        mime="application/pdf",
                    )

        except Exception as e:
            st.error(f"Falhou: {e}")

