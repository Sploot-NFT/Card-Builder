# Card-Builder
turns metadata json into fancy card art.


### TO USE

make sure you have 1) pillow installed, and 2) have some json metadata from the sploot generator.

```
$: pip install pillow
```

then just run the python script.
```
$: python process_cards.py
```

the process looks like this:
```
➜  card-builder git:(main) ✗ python process_cards.py

========= MAIN MENU ===========
a) Create All Cards
-------------------
q) Quit

Which selection? (a): 

Defaulting to `Create All Cards`.

============ PROCESSING CARDS ============
opening metadata: ../sploot-generator/metadata/986.json
saving: cards/986.png

opening metadata: ../sploot-generator/metadata/991.json
saving: cards/991.png

opening metadata: ../sploot-generator/metadata/0.json
saving: cards/0.png

opening metadata: ../sploot-generator/metadata/997.json
saving: cards/997.png


===> Finished.

```
