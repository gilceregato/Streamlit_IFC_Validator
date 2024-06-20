import streamlit as st
import ifcopenshell
import tempfile
import os
from pathlib import Path
import pandas as pd

st.set_page_config(
    page_title="Quantitativos dos elementos - EM DESENVOLVIMENTO",
    page_icon="#️⃣",
    layout="wide"
)

st.markdown(
    '''
   ATENÇÃO: EM DESENVOLVIMENTO!!
'''
)

def ifc_upload ():
#Coleta IFCs por upload
  ifc_files = st.file_uploader('Faça upload do seu IFC',['ifc'], accept_multiple_files=True)
  for uploaded_file in ifc_files:
    bytes_data = uploaded_file.read()
    st.write("Nome do arquivo:", uploaded_file.name)
  ifc_path_list = []
  if ifc_files:
    for ifc in ifc_files:
      temp_dir = tempfile.mkdtemp()
      ifc_path = os.path.join(temp_dir, ifc.name)
      with open(ifc_path, "wb") as f:
        f.write(uploaded_file.getvalue())
      ifc_path_list.append(Path(ifc_path))
  return ifc_path_list

def coleta_propriedades (ifcs):
   for ifc in ifcs:
    model = ifcopenshell.open(ifc)
    elements = ifcopenshell.util.selector.filter_elements(model,'IfcElement')
    st.markdown(f"Existem {len(elements)} elementos no modelo:")

a = ifc_upload()
coleta_propriedades(a)