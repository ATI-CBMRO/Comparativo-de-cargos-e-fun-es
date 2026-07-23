"""Valida o enriquecimento de alternatives no Regimento atual (de-para Bloco D)."""
import json, sys
from pathlib import Path
BASE = Path(__file__).parent.parent
ATU = BASE / "database" / "atual" / "minuta_structure.json"
FUT = BASE / "database" / "minuta_structure.json"

# de-para proposto (atual -> futura); 8 diretos + 11 mapeados; emg/comissoes sem equivalente
DEPARA = {
    "cg":"cg","condeg":"condeg","assessorias":"assessorias","corregedoria":"corregedoria",
    "dp":"dp","deei":"deei","cat":"cat","dlog":"dlog",
    "ajudancia":"ag","gabinete":"gab-cg","cepdec":"depdec","dint":"cint","cpof":"dpof",
    "dcs":"ccs","dinf":"cinf","cob1":"crbm","cob2":"crbm","coa":"boa","gbs":"bbs",
}
def main():
    errs=[]
    atu=json.loads(ATU.read_text(encoding="utf-8"))
    fut=json.loads(FUT.read_text(encoding="utf-8"))
    fut_alt={c.get("organKey"):(c.get("alternatives") or {}) for c in fut["chapters"] if c.get("kind")=="organ"}
    for c in atu["chapters"]:
        if c.get("kind")!="organ": continue
        k=c.get("organKey")
        alt=c.get("alternatives") or {}
        # órgãos com equivalente que TEM Bloco D na futura devem receber alternatives
        fk=DEPARA.get(k)
        if fk and fut_alt.get(fk):
            if not alt:
                errs.append(f"{k}: esperava alternatives (de-para -> {fk}), veio vazio")
            else:
                # verbatim: os excerpts devem ser idênticos aos da futura para a mesma fonte
                for uf, a in alt.items():
                    fa=fut_alt[fk].get(uf)
                    if fa and a.get("excerpts")!=fa.get("excerpts"):
                        errs.append(f"{k}/{uf}: excerpts divergem do Bloco D da futura (deve ser cópia verbatim)")
        # emg/comissoes não podem ganhar alternatives (sem equivalente)
        if k in ("emg","comissoes") and alt:
            errs.append(f"{k}: não deveria ter alternatives (sem equivalente no de-para)")
        # ISOLAMENTO: nenhuma competência do RO pode citar CBM de outro estado
        for s in c.get("sections") or []:
            txt=json.dumps(s, ensure_ascii=False)
            import re
            m=re.search(r"cf\. CBM(?!RO)", txt)
            if m: errs.append(f"{k}: seção do RO cita fonte de outro estado ({m.group(0)}) — vazamento")
    if errs:
        print("FALHOU:"); [print(" -",e) for e in errs[:30]]; sys.exit(1)
    n=sum(1 for c in atu["chapters"] if c.get("kind")=="organ" and (c.get("alternatives") or {}))
    print(f"OK — {n} órgãos do Regimento atual com alternatives (Bloco D reaproveitado), sem vazamento.")
if __name__=="__main__": main()
