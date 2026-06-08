'''

cd info_segugio

poetry install

eval $(poetry env activate)

poetry run chainlit run info_segugio/__init__.py -w

'''