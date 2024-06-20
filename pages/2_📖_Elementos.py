import streamlit as st
import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.selector
import tempfile
import pandas as pd
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
    A validação de elementos permite verificar quais os tipos de elementos (Entities) o IFC possui e quantas ocorrências de cada tipo existem no modelo\n
''')
########

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

def lista_classes_geral (ifcs):
   for ifc in ifcs:
    model = ifcopenshell.open(ifc)
    elements = ifcopenshell.util.selector.filter_elements(model,'IfcElement')
    st.markdown(f"Existem {len(elements)} elementos no modelo:")

#Gera uma lista de classes únicas nos ifcs        
    lista_classes = []
    for element in elements:
        classe_ifc=ifcopenshell.util.selector.get_element_value(element, 'class')
        lista_classes.append(classe_ifc)
    todas_as_classes=lista_classes
    df_todas_as_classes=pd.DataFrame(todas_as_classes)
    lista_classes=set(lista_classes)

    #Adicionando botão para seleção das classes:
    classes_selecionadas = st.sidebar.multiselect('Selecione as classes a contabilizar',lista_classes, lista_classes)

    #a) Quantidades de ocorrências
    quantidades_elementos = []
    for classe in classes_selecionadas:
        elements = ifcopenshell.util.selector.filter_elements(model,classe)
        qtt_element = len(element)
        quantidades_elementos.append(qtt_element)
 
    #Cria DataFrame com todos os parâmetros coletados
    df_lista_classes=pd.DataFrame(classes_selecionadas)
    df_quantidades_elementos = pd.DataFrame(quantidades_elementos)

    df_lista_classes['Classe IFC']=df_lista_classes[0]
    df_lista_classes['Ocorrências']=df_quantidades_elementos
    df_lista_classes=df_lista_classes[['Classe IFC','Ocorrências']]

    #Exibe DataFrame conforme filtros adotados
    st.markdown('Lista de elementos por tipo (classe) e número de ocorrências:')
    st.dataframe(df_lista_classes)

a = ifc_upload()
lista_classes_geral (a)