from openai import OpenAI
from Servicios.FBReadService import FBReadService

class ChatService:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key)
        self.fb = FBReadService()

    def _construir_contexto(self, user_id):
        tiendas = self.fb.obtener_tiendas_por_usuario(user_id)
        ventas = self.fb.obtener_ventas_por_usuario(user_id)

        if not tiendas:
            return "No se encontraron tiendas asociadas a tu cuenta."

        texto = "Información de tus tiendas y productos:\n\n"
        for id_t, t in tiendas.items():
            texto += f"- Tienda: {t.get('nombre')} ({t.get('categoria')})\n"
            texto += f"  Dirección: {t.get('direccion')}\n"

            prods = t.get("productos", {})
            for _, p in prods.items():
                texto += f"   * {p.get('nombre')} - ${p.get('precio')} - stock: {p.get('stock')}\n"
            texto += "\n"

            # Resumen de ventas
            ventas_tienda = ventas.get(id_t, {})
            if ventas_tienda:
                texto += "  Ventas recientes:\n"
                for v_id, v in ventas_tienda.items():
                    texto += f"    - Fecha: {v.get('fecha')}, Total: ${v.get('total')}\n"
            else:
                texto += "  No hay ventas registradas.\n"

            texto += "\n"

        return texto

    def send(self, history, user_id, temperature=0.7, max_tokens=500):
        contexto = self._construir_contexto(user_id)

        mensajes = [
            {"role": "system", "content": "Eres un asistente que ayuda a usuarios a consultar información de SU tienda. No muestres jamás datos de otros usuarios."},
            {"role": "system", "content": contexto},
        ] + history

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensajes,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response.choices[0].message.content
