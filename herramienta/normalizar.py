"""MatIA · Funciones para depurar texto y códigos. Retos 2 y 4."""

TILDES = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U"}


def normalizar_codigo(texto):
    """' bn022r ' -> 'BN022R' ; '8393184.0' -> '8393184' ; '' -> ''."""
    # TODO: Reto 2. strip() quita espacios, upper() pasa a mayúsculas. Si termina en '.0' y lo
    # demás son cifras (isdigit), quitad el '.0'.
    return str(texto)


def normalizar_texto(texto):
    """' Mosquito  curvo ' -> 'MOSQUITO CURVO': mayúsculas, sin tildes, sin espacios sobrantes."""
    # TODO: Reto 2. Recorred las letras de texto.strip().upper() y cambiad las que estén en TILDES.
    # Después, mientras haya '  ' (dos espacios), sustituidlos por uno.
    return str(texto)


def es_codigo_fabricante(codigo):
    """True si el código (ya normalizado) tiene la forma habitual: 2 letras, 3 cifras, 1 letra y
    quizá 1 cifra al final. 'BN022R' -> True ; '8393184' -> False ; 'CONMED' -> False."""
    # TODO: Reto 2. Comprobad la longitud y cada tramo con isalpha() e isdigit().
    # codigo[0:2] son los dos primeros caracteres, codigo[2:5] los tres siguientes…
    return False


def codigo_de_nombre(nombre):
    """'0b181205-NB114R_18_JPG.rf.XYZ' -> 'NB114R'. Formato: hash-CODIGO_indice_...  ('' si no encaja)."""
    # TODO: Reto 4. Mismo código que el martes: split('-', 1) y split('_', 1).
    # Devolved el código ya normalizado con normalizar_codigo.
    return ""


def pruebas_reto2():
    assert normalizar_codigo(" bn022r ") == "BN022R"
    assert normalizar_codigo("8393184.0") == "8393184"
    assert normalizar_codigo("") == ""
    assert normalizar_texto(" Mosquito  curvo ") == "MOSQUITO CURVO"
    assert normalizar_texto("Disección") == "DISECCION"
    assert normalizar_texto("") == ""
    assert es_codigo_fabricante("BN022R") and es_codigo_fabricante("EA831R5")
    assert not es_codigo_fabricante("8393184") and not es_codigo_fabricante("CONMED") and not es_codigo_fabricante("")


def pruebas_reto4():
    assert codigo_de_nombre("0b181205-NB114R_18_JPG.rf.XYZ") == "NB114R"
    assert codigo_de_nombre("CAJA_cirugiaGeneralA_s3_01") == ""
    assert codigo_de_nombre("abc-SINGUIONBAJO") == ""
