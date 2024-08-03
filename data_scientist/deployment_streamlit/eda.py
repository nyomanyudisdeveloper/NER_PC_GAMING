import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load and preprocess the data
df = pd.read_csv('DatasetWithTagFinal.csv')
df.dropna(inplace=True)


def run():
    st.write('### ***Here is Named Entity Recognition Data Set***')
    # Display the dataframe in Streamlit
    st.dataframe(df)

    # Add a markdown separator and title
    st.markdown('---')
    st.write('### ***Top 5 Word Tags in Discussion***')

    # Filter and group the data
    data = df[(df['tag'].str[0] == 'B') | (df['tag'].str[0] == 'O')].groupby('tag').size().sort_values(ascending=False).iloc[:5]
    x = data.index.to_list()
    y = data.values

    # Plot the data using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title("Top 5 Word Tags")
    ax.set_xlabel("Tags")
    ax.set_ylabel("Count")

    # Display the plot in Streamlit
    st.pyplot(fig)
    st.write('Distribusi tag dari jumlah tertinggi ke terendah adalah O, Specs, Game, Request, dan Device. Hal ini disebabkan oleh banyaknya kata dalam data yang tidak memiliki makna khusus terkait PC gaming, sehingga dikategorikan sebagai O. Tag Specs sering muncul karena banyak pengguna tertarik mengetahui spesifikasi optimal untuk menjalankan game favorit mereka. Tag Game menjadi topik yang sering ditanyakan, yang sangat wajar mengingat game merupakan elemen utama yang menarik perhatian pengguna dalam konteks PC gaming. Selanjutnya, tag Request muncul saat pengguna meminta rekomendasi atau informasi spesifik terkait PC gaming. Tag Device muncul karena pengguna sering membahas perangkat keras (hardware) yang digunakan, seperti kartu grafis, CPU, dan perangkat lainnya yang mendukung performa gaming. Distribusi tag ini memberikan gambaran tentang fokus utama dan kebutuhan komunitas PC gaming, membantu dalam memahami tren dan preferensi pengguna.')
    st.markdown('---')

    st.write('### ***Top 5 Specs that People Ask about the Most***')
    
    # Filter and group the data
    data = df[df['tag'] == 'B-Spek'][['kata', 'tag']].groupby('kata').count().sort_values(by='tag', ascending=False).iloc[0:5]
    x = data.index.tolist()
    y = data['tag'].tolist()

    # Plot the data using Matplotlib
    fig, ax = plt.subplots()
    sns.set(style="whitegrid")  # Optional: set seaborn style
    ax.barh(x, y, color='skyblue')
    ax.set_title("Top 5 Specs")
    ax.set_xlabel("Count")
    ax.set_ylabel("Tags")
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    st.write('Top specs yang sering ditanyakan oleh para pengguna adalah video graphic accelerator (VGA). Hal ini wajar karena VGA meningkatkan visual grafis pada game, sehingga memberikan pengalaman bermain yang lebih baik. Selanjutnya, solid state drive (SSD) juga sering ditanyakan, karena SSD membantu meningkatkan performa game, terutama karena saat ini PC gaming memiliki standar untuk memiliki SSD. SSD meningkatkan kecepatan loading game dan sistem secara keseluruhan. Selain itu, Random Access Memory (RAM) juga menjadi bagian yang sangat penting. Semakin besar kapasitas RAM, semakin baik respons sistem dan kecepatan frame rate, dibandingkan dengan sistem yang memiliki memori lebih sedikit. RAM yang lebih besar memungkinkan game dan aplikasi berjalan lebih lancar dan cepat.Prosesor Intel juga sering disebut dalam pertanyaan. Semakin kuat prosesor, semakin cepat komputer menyelesaikan tugas yang diberikan. Intel Core i7 menjadi prosesor minimal yang disarankan untuk bermain game dengan performa lebih baik, karena mampu menangani tugas-tugas berat dan multitasking dengan efisien. Kemudian, hard disk drive (HDD) meskipun sekarang tidak sepopuler SSD, masih digunakan sebagai drive penyimpanan sekunder. HDD menyediakan ruang ekstra sebesar terabyte untuk menyimpan data yang tidak muat di SSD. HDD tetap menjadi pilihan untuk menyimpan data dalam jumlah besar dengan biaya yang lebih ekonomis. Dengan demikian, dapat disimpulkan bahwa VGA, SSD, RAM, prosesor Intel, dan HDD adalah komponen utama yang sering menjadi perhatian para pengguna dalam komunitas PC gaming. Keberadaan komponen-komponen ini sangat berpengaruh terhadap performa dan pengalaman bermain game secara keseluruhan.')
    st.markdown('---')

    st.write('### ***Top 5 Games that People Ask About the Most***')

    # Filter and group the data, then select specific games
    data = df[df['tag'] == 'B-Game'][['kata', 'tag']].groupby('kata').count().sort_values(by='tag', ascending=False)
    data = data.loc[['gta', 'valorant', 'rdr', 'pes', 'roblox']]
    x = data.index.tolist()
    y = data['tag'].tolist()

    # Plot the data using Matplotlib
    fig, ax = plt.subplots()
    sns.set(style="whitegrid")  # Optional: set seaborn style
    ax.pie(y, labels=x, autopct='%1.1f%%', startangle=140)
    ax.set_title("Top 5 Games Mentioned")

    # Display the plot in Streamlit
    st.pyplot(fig)
    st.write('5 Game yang paling sering ditanyakan adalah Grand Theft Auto (GTA), valorant, roblox, Pro Evolution Soccer (PES), dan Read Dead Redemption (RDR), Hal ini wajar dikarenakan game - game tersebut memerlukan PC gaming yang baik, sehingga menjadi tolak ukur')
    st.markdown('---')

    st.write('### ***Top 5 Device that people ask about the most***')
    data = df[df['tag'] == 'B-Device'][['kata','tag']].groupby('kata').count().sort_values(by='tag',ascending=False).iloc[0:5]
    x = data.index.tolist()
    y = data['tag'].tolist()

    # Plot the data using Matplotlib
    fig, ax = plt.subplots()
    sns.set(style="whitegrid")  # Optional: set seaborn style
    ax.barh(x, y, color='darkblue')
    ax.set_title("Top 5 Device")
    ax.set_xlabel("Count")
    ax.set_ylabel("Tags")
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)
    st.write('Device yang paling sering ditanyakan oleh orang adalah monitor, pc, keyboard, mouse, dan fan. Device ini paling sering ditanyakan karena device - device yang umum diketahui oleh orang banyak')
    st.markdown('---')
    st.write('### ***Top 5 Activities that People Ask About the Most***')

    # Normalizing terms in 'kata' column
    df.loc[df['kata'] == 'desain', 'kata'] = 'design'
    df.loc[df['kata'] == 'editing', 'kata'] = 'edit'
    df.loc[df['kata'] == 'rander', 'kata'] = 'render'
    df.loc[df['kata'] == 'live', 'kata'] = 'livestream'

    # Filter and group the data
    data = df[df['tag'] == 'B-Kegiatan'][['kata', 'tag']].groupby('kata').count().sort_values(by='tag', ascending=False).iloc[0:5]
    x = data.index.to_list()
    y = data['tag'].tolist()

    # Plot the data using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(x, y, color='red')
    ax.set_title("Top 5 Activities")
    ax.set_xlabel("Activity")
    ax.set_ylabel("Count")
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)
    st.write('Kegiatan yang paling sering ditanyakan adalah mengedit, livestream, streaming, render, dan record. Kegiatan - kegiatan ini adalah kegiatan yang membutuhkan pc yang kuat, sedangkan rakit itu menjadi pertanyaan yang lumayan sering ditanyakan karena diperlukan dalam perakitan PC')
    st.markdown('---')
if __name__ == '__main__':
    run()
