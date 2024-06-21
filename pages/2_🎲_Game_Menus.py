import time
import random
import logging
import streamlit as st

from utils import *

st.set_page_config(
    page_title="Let the Game Begins..",
    page_icon="🤓",
    layout="wide"
)
hide_st(st)

g_types = get_game_types()
game_types = [g_type[1] for g_type in g_types]

selected_game_type = st.sidebar.selectbox("Pick game type:", game_types)
sidebar_btn_new_games = st.sidebar.button("New Games")
st.session_state['selected_game_type'] = selected_game_type


def new_games():
    st.session_state['game_over'] = False
    if 'secret_number' in st.session_state:
        del st.session_state['secret_number']
    if 'game_history_id' in st.session_state:
        del st.session_state['game_history_id']

def generate_unique_number():
    numbers = list(range(10))  # Angka dari 0 sampai 9
    random.shuffle(numbers)
    return ''.join(map(str, numbers[:4]))  # Mengambil 4 angka unik

if 'is_logged_in' in st.session_state and st.session_state['is_logged_in'] == True:

    if sidebar_btn_new_games:
        new_games()

    if selected_game_type.lower() == 'number':
        st.write("Selamat datang di permainan Angka!")
        
        if 'game_history_id' not in st.session_state:
            st.session_state['game_history_id'] = create_new_game(st.session_state['user_id'], 1)[0][0]

        if 'secret_number' not in st.session_state:
            st.session_state['secret_number'] = generate_unique_number()

        secret_number = st.session_state['secret_number']
        st.caption("Tebak angka 4 digit yang unik. Angka tidak boleh berulang.")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Guess the Number..")
            print(secret_number)
            logging.warning(secret_number)
            
            if 'game_over' not in st.session_state:
                st.session_state['game_over'] = False

            if not st.session_state['game_over']:
                guess = st.text_input("Masukkan tebakan Anda:", max_chars=4, key="guess_input")

                if guess:
                    if guess.isdigit() and len(guess) == 4 and len(set(guess)) == 4:
                        correct_numbers = sum(1 for g in guess if g in secret_number)
                        correct_positions = sum(1 for x, y in zip(guess, secret_number) if x == y)
                        st.error(f"{correct_numbers} angka benar, {correct_positions} posisi benar.")

                        # Menyimpan tebakan ke database
                        save_history_guessing(st.session_state['game_history_id'], st.session_state['user_id'], guess, correct_numbers, correct_positions)

                        if correct_positions == 4:
                            st.session_state['game_over'] = True
                            st.success(f"Selamat! Anda menebak dengan benar setelah {get_total_guessing_in_one_game(st.session_state['game_history_id'], st.session_state['user_id'])[0][0]} kali tebakan.")

                            start_time = time.time()
                            while time.time() - start_time < 3:
                                st.balloons()
                                time.sleep(1)  
                                # Menambahkan jeda 1 detik untuk menghindari terlalu banyak pemanggilan st.balloons secara berlebihan
                    else:
                        st.error("Masukkan harus berupa 4 digit angka yang unik dan tidak berulang.")
            else:
                st.success("Permainan telah selesai. Mulai ulang untuk bermain lagi.")
                new_game = st.button("New Game")
                if new_game:
                    new_games()
                    st.rerun()

        with col2:
            st.write("Guessing Histories:")
            rows = get_guessing_history_current_game(st.session_state['game_history_id'], st.session_state['user_id'])

            data_histories = []
            for row in rows:
                data_histories.append({
                    "tebakan": row[0],
                    "jawaban_benar": row[1],
                    "posisi_benar": row[2]
                })

            # Menampilkan data dalam bentuk tabel
            edited_df = st.data_editor(
                data_histories,
                height=300,
                column_order=['tebakan', 'jawaban_benar', 'posisi_benar'],
                column_config={
                    "tebakan": st.column_config.TextColumn("Tebakan", disabled=True),
                    "jawaban_benar": st.column_config.NumberColumn("Jawaban Benar", disabled=True),
                    "posisi_benar": st.column_config.NumberColumn("Posisi Benar", disabled=True)
                },
                num_rows="fixed",
                use_container_width=True,
                hide_index=True
            )
            
    elif selected_game_type == 'Huruf':
        st.write("Selamat datang di permainan Huruf!")
        # Tempatkan kode untuk permainan Huruf di sini
    elif selected_game_type == 'Kata':
        st.write("Selamat datang di permainan Kata!")
        # Tempatkan kode untuk permainan Kata di sini
else:
    st.warning("Please login first!", icon="⚠️")
