import streamlit as st
import requests 
import pandas as pd
import json
import random
from PIL import Image
st.set_page_config(layout="wide")

#im = Image.open(requests.get('https://nftnow.com/wp-content/uploads/2022/05/Wagmi-San.jpg', stream=True).raw)
#st.image(im)


key="rEBZmMIpWKvEBI6ezQZd9ZQ__1d1iERZ"



st.write('# Dashboard - 10KTF')
address = st.text_input('What is the address?', "0x740C569F20076F1D96be1222240d55A5eED29Df5")
@st.cache
def read_dataframe(address):
    Contract_Addresses=["0xedb61f74b0d09b2558f1eeb79b247c1f363ae452","0x7bd29408f11d2bfc23c34f18275bbf23bb716bc7","0xbd3531da5cf5857e7cfaa92426877b022e612cf8","0x521f9c7505005cfa19a8e5786a9c3c9c9f5e6f42","0x7f36182dee28c45de6072a34d29855bae76dbe2f","0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d","0xba30e5f9bb24caa003e9f2f0497ad287fdf95623","0x60e4d786628fea6478f785a6d7e704777c86a7c6","0x1a92f7381b9f03921564a437210bb9396471050c","0xe785e82358879f061bc3dcac6f0444462d4b5330","0xf61f24c2d93bf2de187546b14425bf631f28d6dc","0x3bf2922f4520a8ba0c2efc3d2a1539678dad5e9d","0x572e33ffa523865791ab1c26b42a86ac244df784","0x1cb1a5e65610aeff2551a50f76a87a7d3fb649c6","0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb","0x23581767a106ae21c074b2276d25e5c3e136a68b","0x251b5f14a825c537ff788604ea1b58e49b70726f","0x0cfb5d82be2b949e8fa73a656df91821e2ad99fd","0xe75ef1ec029c71c9db0f968e389331609312aa22"]
    address_string=""
    for add in Contract_Addresses:
        address_string=address_string+"contractAddresses[]="+add+"&"
    
    headers_alchemy = {"Accept": "application/json"}
    url="https://eth-mainnet.g.alchemy.com/nft/v2/"+str(key)+"/getNFTs?owner="+str(address)+"&pageKey=123456&"+address_string+"withMetadata=true"
    response = requests.get(url, headers=headers_alchemy)
    response_json=json.loads(response.text)
    try:
        next_cursor=response_json["pageKey"]
    except:
        next_cursor=None
    df = pd.json_normalize(response_json['ownedNfts'])
    
    i=0
    while next_cursor!= None and i!=50:
        url="https://eth-mainnet.g.alchemy.com/nft/v2/"+str(key)+"/getNFTs?owner="+str(address)+"&pageKey="+str(next_cursor)+"&"+address_string+"withMetadata=true"
        response = requests.get(url, headers=headers)
        response_json=json.loads(response.text)
        df_cursor = pd.json_normalize(response_json['ownedNfts']) 
        i=i+1
        if i==50:
            print("This owner have a lot of tokens, be careful with the api key costs")
        print(str(i)+","+str(response_json['totalCount']))
        df=pd.concat([df,df_cursor])
        try:
            next_cursor=response_json["pageKey"]
        except:
            break
            
    df=df.reset_index(drop=True)
    df1=df[["contractMetadata.name","title","contract.address","id.tokenId","metadata.image","metadata.attributes"]]
    df2=df1.copy()    
    ID=[]
    for index, row in df2.iterrows():
        ID.append(int(row["id.tokenId"],16))
    df2.insert(loc=3, column="Id", value=ID)
    df2=df2.drop(columns="id.tokenId") 
    return df2

def separate(df_initial):
    options = ['10KTF', '10KTF Combat Gear']  
    df10KTF = df_initial[df_initial['contractMetadata.name'].isin(options)] 
    dfnot10KTF=df_initial[~df_initial['contractMetadata.name'].isin(options)] 
    df10KTF=df10KTF.reset_index(drop=True)
    dfnot10KTF=dfnot10KTF.reset_index(drop=True)
    dfnot10KTF['title'] = dfnot10KTF['title'].apply(lambda x:x.lower())
    TITLE=[]
    for index, row in dfnot10KTF.iterrows():
        if row["title"]=="":
            title=""
            if row["contractMetadata.name"]=="BoredApeKennelClub":
                title="bakc #"+str(row["Id"])
                print(title)

            if row["contractMetadata.name"]=="BoredApeYachtClub":
                title="bayc #"+str(row["Id"])
                print(title)

            if row["contractMetadata.name"]=="MutantApeYachtClub":
                title="mayc #"+str(row["Id"])
                print(title)

            TITLE.append(title)
        elif row["title"]=="cryptopunks":
            TITLE.append("cryptopunk #"+str(row["Id"]))
        elif row["contractMetadata.name"]=="ForgottenRunesWizardsCult":
            TITLE.append("wizard #"+str(row["Id"]))
        elif row["contractMetadata.name"]=="Moonbirds":
            TITLE.append("moonbird #"+str(row["Id"]))
        elif row["contractMetadata.name"]=="0N1 Force":
            TITLE.append("0n1 force #"+str(row["Id"]))
        elif row["contractMetadata.name"]=="ForgottenSouls":
            TITLE.append("soul #"+str(row["Id"]))
        elif row["contractMetadata.name"]=="Wolf Game":
            TITLE.append("wolf game #"+str(row["Id"]))
        elif ("gutter cat" in  row["title"]):
            TITLE.append("gcg #"+str(row["Id"]))

        else:
            TITLE.append(row["title"])
    dfnot10KTF.insert(loc=2, column="title2", value=TITLE)
    df10KTF2=df10KTF.copy()

    Collection=[]
    Parent_Name=[]
    Item=[]
    Type=[]
    Background=[]
    value1=[]
    value2=[]

    for index, row in df10KTF2.iterrows():
        if row["metadata.attributes"]:
            dicionario_metadata = row["metadata.attributes"]
            Collection_row=dicionario_metadata[0]["value"]
            Parent_Name_row=dicionario_metadata[1]["value"]
            Item_row=dicionario_metadata[2]["value"]
            Type_row=dicionario_metadata[3]["value"]
            Background_row=dicionario_metadata[4]["value"]
            value1_row=dicionario_metadata[5]["value"]
            value2_row=dicionario_metadata[6]["value"]
        else:
            ID=row["token_id"]
            token_address=row["token_address"]
            url = "https://api.blockspan.com/v1/nfts/contract/"+str(row["token_address"])+"/token/"+str(row["token_id"])+"?chain=eth-main"
            response = requests.get(url, headers=headers_blockspan)
            if response:
                dicionario_metadata1 = json.loads(response.text)
                if dicionario_metadata1["metadata"]:
                    Collection_row=dicionario_metadata1["metadata"]['attributes'][0]['value']
                    Parent_Name_row=dicionario_metadata1["metadata"]['attributes'][1]['value']
                    Item_row=dicionario_metadata1["metadata"]['attributes'][2]['value']
                    Type_row=dicionario_metadata1["metadata"]['attributes'][3]['value']
                    Background_row=dicionario_metadata1["metadata"]['attributes'][4]['value']
                    value1_row=dicionario_metadata1["metadata"]['attributes'][5]['value']
                    value2_row=dicionario_metadata1["metadata"]['attributes'][6]['value']
                else:  
                    Collection_row=None
                    Parent_Name_row=None
                    Item_row=None
                    Type_row=None
                    Background_row=None
                    value1_row=None
                    value2_row=None
            else:  
                Collection_row=None
                Parent_Name_row=None
                Item_row=None
                Type_row=None
                Background_row=None
                value1_row=None
                value2_row=None 

        Collection.append(Collection_row)
        Parent_Name.append(Parent_Name_row)
        Item.append(Item_row)
        Type.append(Type_row)
        Background.append(Background_row)
        value1.append(value1_row)
        value2.append(value2_row)


    df10KTF2.insert(loc=5, column="Collection", value=Collection)    
    df10KTF2.insert(loc=6, column="Parent Name", value=Parent_Name)    
    df10KTF2.insert(loc=7, column="Type", value=Type)    
    df10KTF2.insert(loc=8, column="Background", value=Background)    
    df10KTF2.insert(loc=9, column="Value1", value=value1)    
    df10KTF2.insert(loc=10, column="Value2", value=value2)  

    df10KTF2=df10KTF2.drop(columns="metadata.attributes")
    df10KTF3=df10KTF2.copy()
    Parentinaddress=[]
    for index, row in df10KTF3.iterrows():
        parent=row["Parent Name"].lower()
        #print(parent[:8])
        Parentinaddress.append((parent in dfnot10KTF["title"].unique()) or (parent in dfnot10KTF["title2"].unique()))

    #Parentinaddress    
    df10KTF3.insert(loc=11, column="Is parent in wallet?", value=Parentinaddress )
    df10KTF4=df10KTF3.copy()
    basepower=[]
    for index, row in df10KTF4.iterrows():
        points=0
        if "Snapback" in row["Collection"]:
            points=18
        elif "Five Panel" in row["Collection"]:
            points=18
        elif "Daypack" in row["Collection"]:
            points=27
        elif "Comfy Hoodie" in row["Collection"]:
            points=21
        elif "Cat Ear Hoodie" in row["Collection"]:
            points=21
        elif "Socks" in row["Collection"]:
            points=15
        elif "High Top" in row["Collection"]:
            points=44
        elif "Sock Full of Doorknobs" in row["Collection"]:
            points=35
        elif "Combat Helmet" in row["Collection"]:
            points=27
        elif "Pilot Helmet" in row["Collection"]:
            points=33
        elif "Kevlar Vest" in row["Collection"]:
            points=31
        elif "Combat Boots" in row["Collection"]:
            points=65
        elif "FO(a)MO Sword" in row["Collection"]:
            points=52
        elif "Flamethrower" in row["Collection"]:
            points=76
        basepower.append(points)
    #basepower    
    df10KTF4.insert(loc=12, column="base power", value=basepower)
    df10KTF5=df10KTF4.copy()
    image=[]
    for index, row in df10KTF5.iterrows():
        if row["metadata.image"][0]=="i":
            image.append("https://ipfs.io/ipfs/"+row["metadata.image"][7:])
        else:
            image.append(row["metadata.image"])
    df10KTF5.insert(loc=4, column="Images", value=image)
    df10KTF5=df10KTF5.drop(columns="metadata.image")
    df10KTF6=df10KTF5.copy()
    Rarity_multiplier=[]

    for index, row in df10KTF6.iterrows():
        mul=0
        if row["Value1"]=="Common":
            mul=1
        elif row["Value1"]=="Uncommon":
            mul=2
        elif row["Value1"]=="Rare":
            mul=4
        elif row["Value1"]=="Epic":
            mul=8
        Rarity_multiplier.append(mul)
    df10KTF6.insert(loc=12, column="Rarity multiplier", value=Rarity_multiplier)
    df10KTF6.rename(columns = {'contractMetadata.name':'Collection name', 'contract.address':'Address'}, inplace = True)
    df10KTF6['Parent Name'] = df10KTF6['Parent Name'].apply(lambda x:x.lower())
    df10KTF7=df10KTF6.copy()
    points=[]
    for index, row in df10KTF7.iterrows():
        points.append(row["Rarity multiplier"]*row["base power"])
    df10KTF7.insert(loc=14, column="points", value=points)
    return df10KTF7,dfnot10KTF
    
def FINAL_result(dfmission10KTF,dfmissionNOT10KTF):
    FINAL=[]
    FINAL2=[]
    while len(dfmissionNOT10KTF)!=0:

        PARENTS=dfmissionNOT10KTF["title2"].unique().tolist()
        #PARENTS.append("blank")
        df_list_for_each_load=[]
        TYPES=['Footwear', 'Bag', 'Headgear', 'Outerwear', 'Hand']
        myTYPES=['Footwear', 'Bag', 'Headgear', 'Outerwear', 'Hand']

        #PARENTS=["meetbit #131"]

        for avatar in PARENTS:
            LIST_Avatar=[]
            for item_type in TYPES:
                list_type=[]
                list_max=[]
                list_avatar_type=[]
                df_type=dfmission10KTF[dfmission10KTF["Type"]==item_type]
                df_type=df_type.sort_values(by=['points'], ascending=False)
                df_type=df_type.reset_index(drop=True)
                for index, row in df_type.iterrows():
                    if item_type in myTYPES:
                        if index==0:
                            list_max.append(row["title"])
                            list_max.append(row["points"])
                            if "gucci" in avatar:
                                list_max.append(row["Parent Name"])
                                list_max.append(0.5)
                                list_max.append("flat")

                            elif avatar=="blank":
                                list_max.append(row["Parent Name"])
                                list_max.append(0)
                                list_max.append("not flat")

                            else:
                                if row["Parent Name"]==avatar:
                                    list_max.append(row["Parent Name"])
                                    list_max.append(0.2)
                                    list_max.append("not flat")

                                else:
                                    list_max.append(row["Parent Name"])
                                    list_max.append(0.1)
                                    list_max.append("not flat")

                        if row["Parent Name"]==avatar:
                            list_avatar_type.append(row["title"])
                            list_avatar_type.append(row["points"])
                            list_avatar_type.append(row["Parent Name"])
                            list_avatar_type.append(0.2)
                            list_avatar_type.append("not flat")

                    else:
                        break

                if len(list_max)!=0:
                    list_type.append(list_max)
                if len(list_avatar_type)!=0:
                    list_type.append(list_avatar_type)
                if len(list_type)==0:
                    LIST_Avatar.append([["None",0,"None",0,""]])
                else:
                    LIST_Avatar.append(list_type)

            value=0
            for a in LIST_Avatar[0]:
                for b in LIST_Avatar[1]:
                    for c in LIST_Avatar[2]:
                        for d in LIST_Avatar[3]:
                            for e in LIST_Avatar[4]:
                                points_total=a[1]+b[1]+c[1]+d[1]+e[1]
                                if a[4]=="flat"or b[4]=="flat" or c[4]=="flat" or d[4]=="flat" or e[4]=="flat":
                                    bonus=1+0.5
                                else:
                                    bonus=round(a[3]+b[3]+c[3]+d[3]+e[3]+1,1)
                                final=round(bonus*points_total,2)
                                if final>value:
                                    value=final
                                    resposta=final
                                    A=a
                                    B=b
                                    C=c
                                    D=d
                                    E=e
            df_list_for_each_load.append([avatar,A,B,C,D,E,resposta])

        df_best_for_each_load=pd.DataFrame(df_list_for_each_load,columns=["parent",'Footwear', 'Bag', 'Headgear', 'Outerwear', 'Hand',"total"])
        df_best_for_each_load=df_best_for_each_load.sort_values(by=['total'], ascending=False)
        df_best_for_each_load=df_best_for_each_load.reset_index(drop=True)
        lista_the_best_for_each_load=[df_best_for_each_load["parent"][0],df_best_for_each_load['Footwear'][0][:3],df_best_for_each_load['Bag'][0][:3],df_best_for_each_load['Headgear'][0][:3],df_best_for_each_load['Outerwear'][0][:3],df_best_for_each_load['Hand'][0][:3],df_best_for_each_load["total"][0]]
        lista_the_best_for_each_load2=[df_best_for_each_load["parent"][0],df_best_for_each_load['Footwear'][0][0],df_best_for_each_load['Bag'][0][0],df_best_for_each_load['Headgear'][0][0],df_best_for_each_load['Outerwear'][0][0],df_best_for_each_load['Hand'][0][0],df_best_for_each_load["total"][0]]
        #df_best.to_excel("Andrew2.xlsx")
        dfmission10KTF=dfmission10KTF[~dfmission10KTF["title"].isin(lista_the_best_for_each_load2)]
        dfmissionNOT10KTF=dfmissionNOT10KTF[~dfmissionNOT10KTF["title2"].isin(lista_the_best_for_each_load2)]
        dfmission10KTF=dfmission10KTF.reset_index(drop=True)
        dfmissionNOT10KTF=dfmissionNOT10KTF.reset_index(drop=True)
        FINAL2.append(lista_the_best_for_each_load)
        FINAL.append(lista_the_best_for_each_load2)
    df_FINAL2=pd.DataFrame(FINAL2,columns=["parent",'Footwear', 'Bag', 'Headgear', 'Outerwear', 'Hand',"total"])
    dfFINALcopy=df_FINAL2.copy()
    n=0
    while n<5000:
        B=dfFINALcopy.copy()

        lin1=random.randint(0, len(B)-1)
        lin2=random.randint(0, len(B)-1)
        while lin1==lin2:
             lin2=random.randint(0, len(B)-1)
        soma1_antes=B.iloc[lin1,6]
        soma2_antes=B.iloc[lin2,6]
        soma_antes_combonus=soma1_antes+soma2_antes
        type_to_change=random.randint(1, 5)
        #type_to_change=4
        teste1=B.iloc[lin1,type_to_change]
        teste2=B.iloc[lin2,type_to_change]
        #print(testea)

        B.iat[lin1,type_to_change]=teste2
        B.iat[lin2,type_to_change]=teste1


        #print(B.iloc[lin1,2])

        bonus_lin1=0
        soma_lin1=0
        for i in range(1,6):
            soma_lin1+=B.iloc[lin1,i][1]
            if "gucci" in B.iat[lin1,i][0]:
                bonus_lin1=0.5
            else:
                if B.iat[lin1,i][0]!="None":
                    if B.iat[lin1,i][2]==B.iat[lin1,0].lower():
                        bonus_lin1+=0.2
                    else:
                        bonus_lin1+=0.1    
                else:
                    bonus_lin1+=0

        bonus_lin2=0
        soma_lin2=0
        for i in range(1,6):
            soma_lin2+=B.iloc[lin2,i][1]
            if "gucci" in B.iat[lin2,i][0]:
                bonus_lin2=0.5
            else:
                if B.iat[lin2,i][0]!="None":
                    if B.iat[lin2,i][2]==B.iat[lin2,0].lower():
                        bonus_lin2+=0.2
                    else:
                        bonus_lin2+=0.1    
                else:
                    bonus_lin2+=0
            
        if soma_lin2*(bonus_lin2+1)+soma_lin1*(bonus_lin1+1)>soma_antes_combonus:
            #print("-")
            B.iat[lin1,6]=round(soma_lin1*(bonus_lin1+1),1)
            B.iat[lin2,6]=round(soma_lin2*(bonus_lin2+1),1)
            dfFINALcopy=B.copy()
       # else:
        #    B.iat[lin1,6]=soma_lin1*(bonus_lin1+1)
        #    B.iat[lin2,6]=soma_lin2*(bonus_lin2+1)
        #    dfFINALcopy=B.copy()
        #print(n)

        n=n+1
    dfFINAL_withloop=dfFINALcopy.copy()
    dfFINAL_withloop["Footwear"] = dfFINAL_withloop["Footwear"].apply(lambda x: x[0])
    dfFINAL_withloop["Bag"] = dfFINAL_withloop["Bag"].apply(lambda x: x[0])
    dfFINAL_withloop["Headgear"] = dfFINAL_withloop["Headgear"].apply(lambda x: x[0])
    dfFINAL_withloop["Outerwear"] = dfFINAL_withloop["Outerwear"].apply(lambda x: x[0])
    dfFINAL_withloop["Hand"] = dfFINAL_withloop["Hand"].apply(lambda x: x[0])


    dfFINAL_withloop=dfFINAL_withloop.sort_values(by=['total'], ascending=False)
    dfFINAL_withloop=dfFINAL_withloop.reset_index(drop=True)
    dfFINAL_withloop=dfFINAL_withloop.round(1)
    dfFINAL_withloop.set_index("parent")
    return dfFINAL_withloop
    


df_initial=read_dataframe(address)
dfmission10KTF,dfmissionNOT10KTF=separate(df_initial)
dfFINAL_withloop=FINAL_result(dfmission10KTF,dfmissionNOT10KTF)
st.write(dfFINAL_withloop.style.format({"total": "{:.1f}"}))
st.write('The total number of points is ', str(round(dfFINAL_withloop['total'].sum(),2)))
