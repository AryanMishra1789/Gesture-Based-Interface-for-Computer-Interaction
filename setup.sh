mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

# Setup LD_LIBRARY_PATH for libGL.so.1
echo "\
export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu\n\
" >> ~/.profile

# Start Xvfb
Xvfb :99 -screen 0 1024x768x16 &

# Set the DISPLAY environment variable
export DISPLAY=:99

source ~/.profile
