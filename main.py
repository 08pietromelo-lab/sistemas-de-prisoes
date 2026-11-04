import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Modal, TextInput, Select, Button
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
# CORRIGIDO: AGORA ACEITA OS NOMES QUE VOCE USOU NO RENDER
CANAL_PAINEL_ID = os.getenv("CANAL_PAINEL") or os.getenv("CANAL_PAINEL_ID")
CANAL_REGISTRO_ID = os.getenv("CANAL_REGISTROS") or os.getenv("CANAL_REGISTRO_ID") or os.getenv("CANAL_JUSTIFICATIVAS_ID")

# --- WEB SERVER PRO RENDER ---
app = Flask('')
@app.route('/')
def home():
    return "Bot de Prisoes Online!"
def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
# ARTIGOS DA POLÍCIA
# ==========================================

ARTIGOS = {
    "01": {
        "nome": "Homicídio Doloso",
        "pena": 40, "reduzida": 32, "aumentada": 52,
        "multa": "R$ 3.500,00"
    },
    "02": {
        "nome": "Tentativa de Homicídio",
        "pena": 30, "reduzida": 24, "aumentada": 39,
        "multa": "R$ 1.500,00"
    },
    "03": {
        "nome": "Homicídio Qualificado",
        "pena": 60, "reduzida": 48, "aumentada": 78,
        "multa": "R$ 7.000,00"
    },
    "04": {
        "nome": "Tráfico de Drogas",
        "pena": 20, "reduzida": 32, "aumentada": 26,
        "multa": "R$ 40 por unidade"
    },
    "05": {
        "nome": "Porte Ilegal de Arma de Fogo",
        "pena": 35, "reduzida": 16, "aumentada": 46,
        "multa": "R$ 2.800,00"
    },
    "06": {
        "nome": "Assalto à Mão Armada",
        "pena": 50, "reduzida": 40, "aumentada": 65,
        "multa": "R$ 2.500,00"
    },
    "07": {
        "nome": "Roubo de Veículo",
        "pena": 30, "reduzida": 28, "aumentada": 39,
        "multa": "R$ 3.000,00"
    },
    "08": {
        "nome": "Furto",
        "pena": 15, "reduzida": 12, "aumentada": 20,
        "multa": "R$ 1.500,00"
    },
    "09": {
        "nome": "Formação de Quadrilha",
        "pena": 35, "reduzida": 28, "aumentada": 46,
        "multa": "R$ 2.500,00"
    },
    "10": {
        "nome": "Corrupção Ativa",
        "pena": 30, "reduzida": 24, "aumentada": 39,
        "multa": "R$ 3.000,00"
    },
    "11": {
        "nome": "Lavagem de Dinheiro",
        "pena": 30, "reduzida": 24, "aumentada": 39,
        "multa": "R$ 3.500,00"
    },
    "12": {
        "nome": "Sequestro",
        "pena": 55, "reduzida": 44, "aumentada": 72,
        "multa": "R$ 4.000,00"
    },
    "13": {
        "nome": "Resistência à Prisão",
        "pena": 15, "reduzida": 12, "aumentada": 20,
        "multa": "R$ 1.500,00"
    },
    "14": {
        "nome": "Desacato à Autoridade",
        "pena": 10, "reduzida": 8, "aumentada": 13,
        "multa": "R$ 1.500,00"
    },
    "15": {
        "nome": "Direção Perigosa",
        "pena": 10, "reduzida": 8, "aumentada": 13,
        "multa": "R$ 2.000,00"
    },
    "16": {
        "nome": "Fuga da Polícia",
        "pena": 15, "reduzida": 12, "aumentada": 20,
        "multa": "R$ 3.000,00"
    },
    "17": {
        "nome": "Estelionato",
        "pena": 30, "reduzida": 24, "aumentada": 39,
        "multa": "R$ 2.500,00"
    },
    "18": {
        "nome": "Contrabando",
        "pena": 30, "reduzida": 24, "aumentada": 39,
        "multa": "R$ 3.500,00"
    },
    "19": {
        "nome": "Atrapalhar Recrutamento",
        "pena": 60, "reduzida": 48, "aumentada": 78,
        "multa": "R$ 1.200,00"
    },
    "20": {
        "nome": "Roubo a Caixinha",
        "pena": 25, "reduzida": 20, "aumentada": 33,
        "multa": "R$ 1.700,00"
    },
    "21": {
        "nome": "Dinheiro Sujo",
        "pena": 25, "reduzida": 20, "aumentada": 33,
        "multa": "R$ 3.000,00",
        "fianca": "R$ 5.000,00"
    },
    "22": {
        "nome": "Corrida Ilegal",
        "pena": 15, "reduzida": 12, "aumentada": 20,
        "multa": "R$ 2.000,00",
        "fianca": "R$ 3.000,00"
    },
    "23": {
        "nome": "Destruição de Patrimônio Público",
        "pena": 20, "reduzida": 16, "aumentada": 26,
        "multa": "R$ 4.500,00"
    },
    "24": {
        "nome": "Roubo a Loja",
        "pena": 30, "reduzida": 24, "aumentada": 39,
        "multa": "R$ 1.500,00"
    },
    "25": {
        "nome": "Roubo ao Banco",
        "pena": 60, "reduzida": 48, "aumentada": 78,
        "multa": "R$ 12.000,00"
    },
    "26": {
        "nome": "Roubo à Joalheria",
        "pena": 60, "reduzida": 48, "aumentada": 78,
        "multa": "R$ 10.000,00"
    },
    "27": {
        "nome": "Tráfico de Armas",
        "pena": 50, "reduzida": 40, "aumentada": 65,
        "multa": "R$ 12.000,00",
        "observacao": "Aplicável a 5 armas ou mais"
    },
    "28": {
        "nome": "Posse de Munição",
        "pena": 10, "reduzida": 8, "aumentada": 13,
        "multa": "R$ 20 por unidade"
    },
    "29": {
        "nome": "Uso Indevido de Canais Públicos",
        "pena": 40, "reduzida": 32, "aumentada": 52,
        "multa": "R$ 2.500,00"
    },
    "30": {
        "nome": "Posse de Ferramentas Ilegais",
        "pena": 15, "reduzida": 12, "aumentada": 20,
        "multa": "R$ 1.800,00",
        "fianca": "R$ 2.600,00"
    },
    "31": {
        "nome": "Ocultação Facial",
        "pena": 25, "reduzida": 20, "aumentada": 33,
        "multa": "R$ 2.000,00",
        "fianca": "R$ 5.000,00"
    }
}

# ==========================================
# FORMULÁRIO DA PRISÃO
# ==========================================

class FormularioPrisao(Modal, title="Registro de Prisão"):

    preso = TextInput(
        label="Nome do indivíduo preso",
        placeholder="Nome no jogo",
        max_length=100
    )

    policial = TextInput(
        label="Policial responsável",
        placeholder="Seu nome",
        max_length=100
    )

    companheiros = TextInput(
        label="Policiais envolvidos",
        placeholder="Nomes ou nenhum",
        required=False,
        max_length=300
    )

    descricao = TextInput(
        label="Descrição da ocorrência",
        placeholder="Explique o motivo da prisão",
        style=discord.TextStyle.paragraph,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        dados = {
            "preso": self.preso.value,
            "policial": self.policial.value,
            "companheiros": self.companheiros.value or "Nenhum",
            "descricao": self.descricao.value
        }

        view = SelecaoArtigos(interaction.client, interaction.channel, dados)

        await interaction.response.send_message(
            "📋 **Selecione os artigos da prisão.**\n"
            "Você pode selecionar vários artigos. Use os botões para mudar de página.",
            view=view,
            ephemeral=True
        )

# ==========================================
# MENU DE ARTIGOS COM PAGINAÇÃO
# ==========================================

class MenuArtigos(Select):

    def __init__(self, view_principal):
        self.view_principal = view_principal

        inicio = view_principal.pagina * 25
        fim = inicio + 25
        codigos = list(ARTIGOS.keys())[inicio:fim]

        opcoes = []

        for codigo in codigos:
            artigo = ARTIGOS[codigo]

            opcoes.append(
                discord.SelectOption(
                    label=f"Art. {codigo}/2025 - {artigo['nome']}",
                    description=f"Pena: {artigo['pena']} min | Multa: {artigo['multa']}",
                    value=codigo
                )
            )

        super().__init__(
            placeholder=f"Página {view_principal.pagina + 1} - Escolha os artigos",
            min_values=1,
            max_values=len(opcoes),
            options=opcoes
        )

    async def callback(self, interaction: discord.Interaction):
        for codigo in self.values:
            if codigo not in self.view_principal.selecionados:
                self.view_principal.selecionados.append(codigo)

        await interaction.response.edit_message(
            content=self.view_principal.mensagem_selecao(),
            view=self.view_principal
        )

class SelecaoArtigos(View):

    def __init__(self, bot, canal, dados):
        super().__init__(timeout=600)

        self.bot = bot
        self.canal = canal
        self.dados = dados
        self.pagina = 0
        self.selecionados = []

        self.atualizar_menu()

    def atualizar_menu(self):
        self.clear_items()

        self.add_item(MenuArtigos(self))

        voltar = Button(
            label="Página anterior",
            emoji="⬅️",
            style=discord.ButtonStyle.secondary,
            disabled=self.pagina == 0
        )
        voltar.callback = self.voltar
        self.add_item(voltar)

        avancar = Button(
            label="Próxima página",
            emoji="➡️",
            style=discord.ButtonStyle.secondary,
            disabled=self.pagina == 1
        )
        avancar.callback = self.avancar
        self.add_item(avancar)

        finalizar = Button(
            label="Finalizar seleção",
            emoji="✅",
            style=discord.ButtonStyle.success
        )
        finalizar.callback = self.finalizar
        self.add_item(finalizar)

    def mensagem_selecao(self):
        if not self.selecionados:
            return "📋 **Selecione os artigos da prisão.**"

        linhas = []

        for codigo in self.selecionados:
            artigo = ARTIGOS[codigo]
            linhas.append(
                f"• Art. {codigo}/2025 — {artigo['nome']} "
                f"({artigo['pena']} min)"
            )

        return (
            "📋 **Artigos selecionados:**\n"
            + "\n".join(linhas)
            + "\n\nContinue selecionando ou clique em **Finalizar seleção**."
        )

    async def voltar(self, interaction: discord.Interaction):
        self.pagina = 0
        self.atualizar_menu()
        await interaction.response.edit_message(
            content=self.mensagem_selecao(),
            view=self
        )

    async def avancar(self, interaction: discord.Interaction):
        self.pagina = 1
        self.atualizar_menu()
        await interaction.response.edit_message(
            content=self.mensagem_selecao(),
            view=self
        )

    async def finalizar(self, interaction: discord.Interaction):
        if not self.selecionados:
            await interaction.response.send_message(
                "Selecione pelo menos um artigo.",
                ephemeral=True
            )
            return

        await interaction.response.edit_message(
            content="✅ Seleção concluída! Vou preparar o registro.",
            view=None
        )

        await publicar_prisao(
            self.bot,
            self.canal,
            self.dados,
            self.selecionados,
            interaction.user
        )

# ==========================================
# PUBLICAÇÃO DO REGISTRO - CORRIGIDO
# ==========================================

async def publicar_prisao(bot, canal_original, dados, selecionados, usuario):

    await canal_original.send(
        f"📸 **{usuario.mention}, envie a foto da prisão neste canal.**\n"
        "A foto é opcional. Se não enviar em até 5 minutos, "
        "o registro será publicado sem ela."
    )

    foto = None

    def verificar(mensagem):
        return (
            mensagem.author.id == usuario.id
            and mensagem.channel.id == canal_original.id
            and len(mensagem.attachments) > 0
        )

    try:
        mensagem = await bot.wait_for(
            "message",
            check=verificar,
            timeout=300
        )
        foto = mensagem.attachments[0].url
    except asyncio.TimeoutError:
        pass

    canal_destino = canal_original

    if CANAL_REGISTRO_ID:
        try:
            canal_encontrado = bot.get_channel(int(CANAL_REGISTRO_ID))
            if canal_encontrado:
                canal_destino = canal_encontrado
        except ValueError:
            canal_destino = canal_original

    if canal_destino is None:
        canal_destino = canal_original

    embed = discord.Embed(
        title="🚔 REGISTRO DE PRISÃO",
        color=discord.Color.dark_blue()
    )

    embed.add_field(
        name="👤 Indivíduo preso",
        value=dados["preso"],
        inline=True
    )

    embed.add_field(
        name="👮 Policial responsável",
        value=dados["policial"],
        inline=True
    )

    embed.add_field(
        name="👥 Policiais envolvidos",
        value=dados["companheiros"],
        inline=False
    )

    embed.add_field(
        name="📝 Descrição da ocorrência",
        value=dados["descricao"],
        inline=False
    )

    linhas_artigos = []
    pena_total = 0

    for codigo in selecionados:
        artigo = ARTIGOS[codigo]
        pena_total += artigo["pena"]

        linha = (
            f"**Art. {codigo}/2025 — {artigo['nome']}**\n"
            f"Pena: {artigo['pena']} min | "
            f"Reduzida: {artigo['reduzida']} min | "
            f"Aumentada: {artigo['aumentada']} min\n"
            f"Multa: {artigo['multa']}"
        )

        if "fianca" in artigo:
            linha += f" | Fiança: {artigo['fianca']}"

        if "observacao" in artigo:
            linha += f"\n⚠️ {artigo['observacao']}"

        linhas_artigos.append(linha)

    embed.add_field(
        name="⚖️ Artigos aplicados",
        value="\n\n".join(linhas_artigos),
        inline=False
    )

    embed.add_field(
        name="⏱️ Soma das penas normais",
        value=f"**{pena_total} minutos**",
        inline=False
    )

    embed.set_footer(
        text=f"Registrado por {usuario.display_name}"
    )

    if foto:
        embed.set_image(url=foto)

    await canal_destino.send(embed=embed)

    await canal_original.send(
        "✅ **Registro de prisão publicado com sucesso!**"
    )

# ==========================================
# PAINEL FIXO
# ==========================================

class PainelPrisoes(View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Registrar Prisão",
        emoji="🚔",
        style=discord.ButtonStyle.primary,
        custom_id="painel:registrar_prisao"
    )
    async def registrar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.send_modal(FormularioPrisao())

# ==========================================
# COMANDO PARA CRIAR O PAINEL
# ==========================================

@bot.tree.command(
    name="painel",
    description="Publica o painel de registro de prisões"
)
async def painel(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        embed = discord.Embed(
            title="📋 PAINEL DE PRISÃO",
            description="Clique no botão abaixo para registrar uma prisão.",
            color=0x2B2D31
        )
        # Aqui usa sua View que já existe no código
        view = PainelView() # se o nome for diferente, me fala
        await interaction.channel.send(embed=embed, view=view)
        await interaction.followup.send("✅ Painel publicado com sucesso!", ephemeral=True)
    except Exception as e:
        print(f"ERRO PAINEL: {e}")
        await interaction.followup.send(f"❌ Erro: {e}", ephemeral=True)

    embed = discord.Embed(
        title="🚔 CENTRAL DE REGISTRO DE PRISÕES",
        description=(
            "Utilize o botão abaixo para registrar uma prisão.\n\n"
            "📋 Preencha os dados da ocorrência.\n"
            "⚖️ Selecione os artigos aplicados.\n"
            "📸 Envie a foto da prisão, se desejar.\n\n"
            "O registro será publicado automaticamente."
        ),
        color=discord.Color.dark_blue()
    )

    await interaction.response.send_message(
        embed=embed,
        view=PainelPrisoes()
    )

# ==========================================
# INICIALIZAÇÃO
# ==========================================

@bot.event
async def setup_hook():
    bot.add_view(PainelPrisoes())
    await bot.tree.sync()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user} | Painel: {CANAL_PAINEL_ID} | Registro: {CANAL_REGISTRO_ID}")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não foi encontrado no arquivo .env")

keep_alive()
bot.run(TOKEN)
