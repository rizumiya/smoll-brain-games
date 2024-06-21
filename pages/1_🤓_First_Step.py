import streamlit as st

from utils import *

st.set_page_config(
    page_title="Be One of Us Now!",
    page_icon="🤓",
)
hide_st(st)

st.subheader("🤔 Who Are You Again?")

tabs = st.tabs(['🤓 Sign In', '🪪 Sign Up', '🤡 Continue as Guest'])

with tabs[0]:
    with st.form('sign_in_form'):   
        st.text_input(
            'Username', 
            key='sign_in_username',
            placeholder='clownMaster69'
        )
        st.text_input(
            'Password', 
            key='sign_in_password', 
            type='password',
            placeholder='YourMomWeight'
        )

        sign_in_btn = st.form_submit_button('Sign In', type='primary')
        if sign_in_btn:
            if not (st.session_state['sign_in_username'] and st.session_state['sign_in_password']):
                st.error('With your current level of stupidity, you are not qualified for this game!', icon="🙅‍♂️")
            else:
                user_id = check_player_credential(
                    st.session_state['sign_in_username'], 
                    st.session_state['sign_in_password']
                )
                if user_id:
                    # add to session state
                    st.session_state['user_id'] = user_id[0][0]
                    st.session_state['is_logged_in'] = True
                    st.success('Welcome back King!, You may proceed to the next step..', icon='🤓')
                else:
                    st.error('Invalid Credentials', icon="⛔️")


with tabs[1]:
    with st.form('sign_up_form'):   
        st.text_input(
            'Display Name', 
            key='sign_up_alias', 
            help='Will be displayed on the leaderboard',
            placeholder='Kong - The Dong Destroyer'
        )
        st.text_input(
            'Username', 
            key='sign_up_username',
            placeholder='clownMaster69'
        )
        st.text_input(
            'Password', 
            key='sign_up_password', 
            type='password',
            placeholder='YourMomWeight'
        )

        sign_up_btn = st.form_submit_button('Sign Up', type='primary')
        if sign_up_btn:
            if not (st.session_state['sign_up_alias'] and 
                    st.session_state['sign_up_username'] and
                    st.session_state['sign_up_password']
                    ):
                st.error('You\'re not nerd enough to sign up', icon="⛔️")
            else:
                if insert_new_player(
                    st.session_state['sign_up_alias'], 
                    'user',
                    st.session_state['sign_up_username'], 
                    st.session_state['sign_up_password']
                ):
                    st.success('Welcome aboard!', icon='🎉')
                else:
                    st.error('Username occupied', icon="⛔️")


with tabs[2]:
    st.write(
        """
        Seriously, are you okay with being a ghost player? Continuing as a guest means your progress will vanish into thin air and your name won't even make it to the leaderboard. 

        What's the point of playing if you're not going to take credit for your wins? Create an account and show the world what you're made of. 
        Don't waste your time playing in obscurity.
        
        or..

        You're just stupid? 🤔
        """.replace("    ", "")
        )
    st.button('Continue as Guest', key='guest_btn')
