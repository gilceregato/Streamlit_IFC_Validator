import streamlit as st
import ifcopenshell
import tempfile
import os
import pystache
from pathlib import Path
from ifctester import ids, reporter

st.set_page_config(
    page_title="Validação utilizando IDS - EM DESENVOLVIMENTO",
    page_icon="✅",
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

def ids_upload ():
#Coleta IDS por upload
  ids_file = st.file_uploader('Faça upload do seu IDS (aceita apenas um arquivo)',['ids'], accept_multiple_files=False)
  ids_path_list = []
  if ids_file:
    ids_file.read()
    st.write("Nome do IDS:", ids_file.name)
    temp_dir = tempfile.mkdtemp()
    ids_path = os.path.join(temp_dir, ids_file.name)
    with open(ids_path, "wb") as f:
      f.write(ids_file.getvalue())
    ids_path_list.append(Path(ids_path))
    return ids_file

def validacao_ids(ifc_path_list, ids_file):
  if ifc_path_list:
    if ids_file:
      for ifcs in ifc_path_list:
        model = ifcopenshell.open(ifcs)
        my_ids = ids.Ids(ids_file)
        my_ids.validate(model)

        temp_dir = tempfile.mkdtemp()
        report_path_txt = os.path.join(temp_dir, 'txt_report.txt')
        reporter.Txt(my_ids).to_file(report_path_txt)
        st.write(f'TXT salvo em: {report_path_txt}')

a = ifc_upload()
b = ids_upload()
validacao_ids(a,b)