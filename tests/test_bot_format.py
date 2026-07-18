from types import SimpleNamespace

from bot.telegram_bot import DISCLAIMER, format_medicine_response


def test_bot_response_includes_medical_disclaimer():
    medicine = SimpleNamespace(
        nombre_medicamento="ACETAMINOFEN",
        estado_registro="Vigente",
        registro_invima="INVIMA 2020M",
        para_que_sirve="Dolor y fiebre",
        efectos_secundarios="Nauseas",
    )

    response = format_medicine_response("acetaminofen", [medicine])

    assert "Registro INVIMA: INVIMA 2020M" in response
    assert DISCLAIMER in response
