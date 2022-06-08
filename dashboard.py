import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title='DeJa Vu Stores', page_icon="🦈")

path = "./data/dataonline.csv"
st.sidebar.title('DeJa Vu Stores')
data = st.sidebar.file_uploader('Upload Dataset', type=['csv'])


# Load the DataFrame
@st.cache
def load_data(dataframe):
    df = pd.read_csv(dataframe, encoding='ISO-8859-1', low_memory=False)
    df["Revenue"] = df['UnitPrice'] * df['Quantity']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['InvoiceMonth'] = df.InvoiceDate.dt.month
    df['InvoiceYear'] = df['InvoiceDate'].dt.year
    return df


# Uploaded
if data is not None:
    df_loaded = load_data(data)
# Default
else:
    df_loaded = load_data(path)

# Menu
menu_options = ['Business Snapshot', 'Analysis', 'About']
selection = st.sidebar.selectbox('Key Performance Indicators (KPIs): ', menu_options)
st.sidebar.write("""Retail Analytics is the process of providing analytical data in inventory levels,
supply chain movement, consumer demand, sales, etc... The analytics on demand and supply data can be used for 
maintaining procurement levels and also infor marketing strategies""")

if selection == 'Business Snapshot':
    st.subheader('Display Data')
    st.dataframe(df_loaded.head())

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Monthly Revenue Overview')
        df_revenue = df_loaded.groupby(["InvoiceMonth", "InvoiceYear"])["Revenue"].sum().reset_index()
        plt.Figure(figsize=(15, 8))
        sns.barplot(x=df_revenue["InvoiceMonth"], y=df_revenue['Revenue']/1000000, hue=df_revenue['InvoiceYear'])
        plt.title('Monthly Revenue')
        plt.xlabel('Month')
        plt.ylabel('Revenue (in Millions)')
        plt.legend(loc='upper left')
        st.pyplot(plt)

    # Col 2
    with col2:
        # Monthly Items Sold Overview
        st.subheader('Monthly Items sold Overview')
        df_quantity = df_loaded.groupby(["InvoiceMonth", "InvoiceYear"])["Quantity"].sum().reset_index()
        plt.Figure(figsize=(15, 8))
        sns.barplot(x="InvoiceMonth", y='Quantity', hue='InvoiceYear', data=df_quantity)
        plt.title('Monthly Items Sold')
        plt.xlabel('Month')
        plt.ylabel('Items Sold')
        plt.legend(loc='upper left')
        st.pyplot(plt)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader('Monthly Active Customers')
        # Monthly Active Customers
        df_active = df_loaded.groupby(["InvoiceMonth", "InvoiceYear"])["CustomerID"].nunique().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="CustomerID", hue="InvoiceYear", data=df_active)
        plt.title("Monthly Active Users")
        plt.xlabel("Month")
        plt.ylabel("Active Users")
        st.pyplot(plt)

    with col4:
        # Monthly Average Revenue
        st.subheader("Average Revenue per Month")
        df_revenue_avg = df_loaded.groupby(["InvoiceMonth", "InvoiceYear"])["Revenue"].mean().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="Revenue", hue='InvoiceYear', data=df_revenue)
        plt.title("Monthly Average Revenue ")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        st.pyplot(plt)

    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Best Countries (Revenue)")
        df_sales = df_loaded.groupby('Country').Revenue.sum().reset_index()
        df_sales.columns = ['Country', 'Sales']
        df_sales.sort_values(by='Sales', inplace=True, ascending=False)
        df_sales.reset_index(inplace=True, drop=True)
        top_5_sales = df_sales.iloc[:5]
        plt.figure(figsize=(15, 10))
        plt.pie(top_5_sales['Sales'],
                labels=top_5_sales['Country'],
                wedgeprops={'edgecolor': 'black'},
                startangle=90,
                radius=1.1,
                counterclock=False,
                autopct='%1.1f%%'
                )
        plt.title('Best performing Countries')
        st.pyplot(plt)

    with col6:
        st.subheader("Worst Countries (Revenue)")
        bottom_5_sales = df_sales.iloc[-5:]
        plt.figure(figsize=(15, 10))
        plt.pie(bottom_5_sales['Sales'],
                labels=bottom_5_sales['Country'],
                wedgeprops={'edgecolor': 'black'},
                startangle=90,
                radius=1.1,
                counterclock=False,
                autopct='%1.1f%%'
                )
        plt.title('Best performing Countries')
        st.pyplot(plt)

    # New vs Existing Users
    st.header("New vs Existing Users")
    df_first_purchase = df_loaded.groupby(["CustomerID"])["InvoiceDate"].min().reset_index()
    df_first_purchase.columns = ["CustomerID", "FirstPurchaseDate"]
    df = pd.merge(df_loaded, df_first_purchase, on="CustomerID")
    df["UserType"] = "New"
    df.loc[df["InvoiceDate"] > df["FirstPurchaseDate"], "UserType"] = "Existing"

    df.head()
    # New vs Existing User Revenue Analysis
    df_new_revenue = df.groupby(["InvoiceMonth", "InvoiceYear", "UserType"])["Revenue"].sum().reset_index()
    plt.figure(figsize=(30, 20))
    sns.relplot(x="InvoiceMonth", y="Revenue", hue="UserType", data=df_new_revenue, kind="line", height=12,
                aspect=18 / 10)
    plt.title("New vs Existing Customer Revenue Overview")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    st.pyplot(plt)

elif selection == 'Analysis':
    st.subheader('Display data')
    st.write(df_loaded.head(5))
    # shape of data
    if st.checkbox("show shape "):
        st.write('Data Shape')
        st.write('{:,} rows; {:,} columns'.format(df_loaded.shape[0], df_loaded.shape[1]))

        # data description
        st.markdown("Descriptive statistics ")
        st.write(df_loaded.describe())

# adding html  Template
footer_temp = """
<!-- CSS  -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" 
type="text/css" rel="stylesheet" media="screen,projection"/>
<link href="static/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" 
integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">
<footer class="page-footer grey darken-4">
<div class="container" id="aboutapp">
<div class="row">
<div class="col l6 s12">
<h5 class="white-text">Retail Analysis App</h5>
<h6 class="grey-text text-lighten-4">This is Africa Data School Streamlit Class practical.</h6>
<p class="grey-text text-lighten-4">April 2022 Cohort</p>
</div>
<div class="col l3 s12">
<h5 class="white-text">Connect With Us</h5>
<ul>
<a href="https://www.facebook.com/AfricaDataSchool/" target="_blank" class="white-text">
<i class="fab fa-facebook fa-4x"></i>
</a>
<a href="https://www.linkedin.com/company/africa-data-school" target="_blank" class="white-text">
<i class="fab fa-linkedin fa-4x"></i>
</a>
<a href="https://www.youtube.com/watch?v=ZRdlQwNTJ7o" target="_blank" class="white-text">
<i class="fab fa-youtube-square fa-4x"></i>
</a>
<a href="https://github.com/Africa-Data-School" target="_blank" class="white-text">
<i class="fab fa-github-square fa-4x"></i>
</a>
</ul>
</div>
</div>
</div>
<div class="footer-copyright">
<div class="container">
Made by <a class="white-text text-lighten-3" href="https://africadataschool.com/">Regan </a><br/>
<a class="white-text text-lighten-3" href="https://africadataschool.com/"></a>
</div>
</div>
</footer>
"""
if selection == 'About':
    st.header('About App')
    components.html(footer_temp, height=500)

