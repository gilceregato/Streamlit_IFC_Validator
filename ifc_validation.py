''' Projeto para validaro arquivo IFC que for colocado em upload'''
import ifcopenshell
import streamlit as st
import tempfile
import os
from pathlib import Path


st.set_page_config(
    page_title="Validação de IFCs",
    page_icon="💻",
    layout="wide"
)

####Sidebar
st.markdown('# Validação básica de arquivos IFC')
st.sidebar.markdown(':blue[Desenvolvido por Gilmar Ceregato]')
#criando um botão que acessa o link dos dados
btn = st.sidebar.link_button('Acesse as especificações dos schemas IFC','https://technical.buildingsmart.org/standards/ifc/ifc-schema-specifications/' )

#####Cabeçalho do Dash
st.markdown(
    '''
    A validação de arquivos IFC é um script básico gerado com ifcopenshell que permite classificar arquivos IFC enviados
    Atualmente ele é capaz de: \n
    1- Validar o schema IFC de arquivos de até 200 Mb, diferenciando IFC 2x3, IFC 4 ou IFC 4x3
'''
)

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

def schema_ifc_padrao ():
  schema_ifc = st.selectbox("Qual é o schema IFC definido no BEP para os arquivos?", ('IFC2x3', 'IFC4', 'IFC4x3'))
  st.write(f'Você selecionou o schema: {schema_ifc}')
  return schema_ifc


def valida_schema (ifc_path_list,schema_ifc):

    for ifc in ifc_path_list:
      open_ifc = ifcopenshell.open(ifc)
      ifc_schema = open_ifc.schema # deve retornar IFC2X3, IFC4, or IFC4X3.
      ifc_name = ifc.stem
      if ifc_schema != schema_ifc:
        st.write(f':red[Erro! O arquivo tem {ifc_schema}. O esquema deveria ser {schema_ifc}]')
        st.success(':red[A validação não foi bem sucedida!]', icon="❌")
      else:
        st.write(f':green[Arquivo {ifc_name} encontrado | Schema: {ifc_schema}]')
        st.success(':green[A validação foi bem sucedida!]', icon="✅")

a = ifc_upload()
b = schema_ifc_padrao()
valida_schema(a, b)