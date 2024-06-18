import streamlit as st
import ifcopenshell
import tempfile
import os
from pathlib import Path

st.set_page_config(
    page_title="Validação de Elementos Existentes",
    page_icon="📖",
    layout="wide"
)

####Sidebar
st.markdown('# Validação de Elementos Existentes')
st.sidebar.markdown(':blue[Desenvolvido por Gilmar Ceregato]')
#criando um botão que acessa o link dos dados
btn = st.sidebar.link_button('Acesse as especificações dos schemas IFC','https://technical.buildingsmart.org/standards/ifc/ifc-schema-specifications/' )

#####Cabeçalho do Dash
st.markdown(
    '''
    A validação de elementos permite verificar se os arquivos possuem:\n
    - Paredes (IfcWall)\n
    - Pisos (IfcSlab)\n
    - Janelas (IfcWindow)
''')

def ifc_upload ():
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

def valida_paredes (ifcs):
    st.markdown('#1. Validação de paredes:')
    for ifc in ifcs:
        open_ifc = ifcopenshell.open(ifc)
        element= open_ifc.by_type('IfcWall')
        ifc_name = ifc.stem        
        if len(element) > 0:
            st.success(f":green[O arquivo {ifc_name} tem {len(element)} paredes]", icon="✅") 
        if len(element) <= 0:
            st.success(f':red[O arquivo {ifc_name} NÃO TEM paredes]', icon="❌")

def valida_janelas (ifcs):
    st.markdown('#2. Validação de janelas:')
    for ifc in ifcs:
        open_ifc = ifcopenshell.open(ifc)
        element= open_ifc.by_type('IfcWindow')
        ifc_name = ifc.stem        
        if len(element) > 0:
            st.success(f":green[O arquivo {ifc_name} tem {len(element)} paredes]", icon="✅") 
        if len(element) <= 0:
            st.success(f':red[O arquivo {ifc_name} NÃO TEM paredes]', icon="❌")

def valida_pisos (ifcs):
    st.markdown('#2. Validação de janelas:')
    for ifc in ifcs:
        open_ifc = ifcopenshell.open(ifc)
        element= open_ifc.by_type('IfcSlab')
        ifc_name = ifc.stem        
        if len(element) > 0:
            st.success(f":green[O arquivo {ifc_name} tem {len(element)} paredes]", icon="✅") 
        if len(element) <= 0:
            st.success(f':red[O arquivo {ifc_name} NÃO TEM paredes]', icon="❌")


a = ifc_upload()
valida_paredes(a)
valida_janelas(a)
valida_pisos(a)