import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from main import process_class, mix_students, make_html

st.title("Teacher's Spot")

st.subheader("Умный сервис для учителей")
st.write("""Ресурс, находящийся перед Вами, позволяет автоматизировать процесс рассадки учеников в классе.
\nПросто следуйте инструкциям ниже.
\n**Работайте, не отвлекаясь от главного!**""")
with st.expander("ИНСТРУКЦИЯ"):
    st.write("""
    \n1) Выберите способ, с помощью которого хотите внести данные в систему.
    \n2.1) При выборе варианта "ввести информацию вручную" введите количество учеников в классе и нажмите клавишу Enter либо используйте кнопки +/-. Затем в открывшихся для заполнения формах запишите данные о каждом ученике: имя и фамилия, есть ли проблемы со зрением/слухом, пол, рука, которой ребёнок пишет, а также рост. Важно, что заполнив форму, необходимо обязательно сохранить информацию, нажав на кнопку «Отправить форму».
    \n2.2) В случае с вариантом "загрузить из файла" нужно будет выбрать соответствующий документ на компьютере. **Важно!** При первом запуске сервиса нельзя загружать файл с данными: сперва нужно заполнить все формы, скачать на устройство таблицу и только потом её переиспользовать.
    \n3) Для проверки валидности данных Вы можете поставить галочку возле «Показать список класса».
    \n4) Финальный шаг: кликните на «Сгенерировать рассадку», чтобы получить план рассадки учеников. Генерировать варианты можно неограниченное количество раз!
    """)

if __name__ == "__main__":

    my_class = pd.DataFrame()

    input_info = st.selectbox("Формат загрузки данных:", options=["ввести информацию вручную", "загрузить из файла"])
    if input_info == "загрузить из файла":
        uploaded_file = st.file_uploader("Выберите файл с расширением .csv, содержащий данные об учениках", type="csv")
        if uploaded_file:
            my_class = pd.read_csv(uploaded_file)
    else:
        my_class = pd.DataFrame(
            columns=["Имя учащегося", "Пол", "Преобладающая рука", "Проблемы со зрением/слухом", "Рост"])

        number = st.number_input("Количество учеников:", max_value=30)

        with st.expander("Добавить информацию", expanded=True):
            for idx in range(number):
                with st.form(key=f"student_form{idx}", clear_on_submit=False):
                    name = st.text_input("Введите имя и фамилию учащегося")
                    vision = st.checkbox("Проблемы со зрением/слухом")
                    gender = st.radio("Укажите пол", options=["М", "Ж"])
                    hand = st.radio("Преобладающая рука", options=["правая", "левая"])
                    height = st.radio("Рост", options=["низкий", "средний", "высокий"])
                    student = pd.DataFrame.from_records(
                        {"Имя учащегося": [name], "Пол": [gender], "Преобладающая рука": [hand],
                         "Проблемы со зрением/слухом": [vision], "Рост": [height]}
                    )
                    submit_button = st.form_submit_button("Отправить форму")
                    my_class = pd.concat([my_class, student])
                    if submit_button:
                        st.success(f"Данные об ученике {name} успешно сохранены!")

    if not my_class.empty and not list(my_class) == ["Имя учащегося", "Пол", "Преобладающая рука", "Проблемы со зрением/слухом", "Рост"]:
        st.warning("Неподдерживаемый формат данных. Попробуйте загрузить другой файл.")
    else:
        result = st.checkbox("Показать список класса")
        if result:
            my_class = my_class.sort_values("Имя учащегося")
            my_class.index = my_class.reset_index(drop=True).index + 1
            st.table(my_class)

        csv = my_class.to_csv(index=False)

        st.download_button(
            label="Скачать данные о классе",
            data=csv,
            file_name="class_list.csv",
            mime="text/csv",
        )

        mix = st.button("Сгенерировать рассадку")
        if mix:
            generation = []
            students = process_class(my_class)
            for idx, group in enumerate(students):
                if not group.empty:
                    generation.extend(mix_students(group))
            components.html(make_html(generation), width=1000, height=1000)
