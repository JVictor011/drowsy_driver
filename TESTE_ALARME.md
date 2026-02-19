# Como Testar o Alarme de Sonolência

## Configurações Atuais (para testes facilitados)

- **PERCLOS Threshold**: 0.50 (50% dos olhos fechados)
- **Persistence**: 3 segundos (antes era 8)
- **Window**: 12 segundos
- **Cooldown**: 3 segundos entre alarmes

## Como Ativar o Alarme

### Método 1: Teste Rápido (Fechar os Olhos)
1. Execute o aplicativo: `python run.py`
2. Olhe para a câmera e **feche os olhos por 3-4 segundos**
3. O valor PERCLOS deve subir rapidamente
4. Quando PERCLOS ≥ 0.50 e duração ≥ 3s, você verá:
   - 🚨 Mensagem no console: "ALERTA! PERCLOS=0.XX >= 0.5"
   - Estado mudará para "DROWSY" (vermelho)
   - **Você ouvirá 3 beeps de 1000Hz**
   - Um MessageBeep do Windows

### Método 2: Piscar Lentamente
1. Pisque MUITO lentamente, mantendo os olhos fechados por mais tempo
2. Faça isso por pelo menos 3-5 segundos
3. Observe o valor PERCLOS subir

## Indicadores Visuais na Tela

- **PERCLOS em BRANCO**: Normal (< 35% do threshold)
- **PERCLOS em AMARELO**: Aviso (≥ 35% do threshold)
- **PERCLOS em LARANJA**: Crítico mas ainda sem persistência
- **PERCLOS em VERMELHO**: Alarme ativo!

O formato na tela é:
```
PERCLOS(12s): 0.XX / 0.50 [X.Xs]
              ^^^^   ^^^^   ^^^^
              atual  limite duração
```

## Teste do Beep Isolado

Para testar apenas o som do alarme:
```bash
python test_beep.py
```

Você deve ouvir:
1. Um MessageBeep do Windows (som de exclamação)
2. 3 beeps curtos de 1000Hz

## Calibração (Opcional)

Pressione **'c'** durante a execução para calibrar o threshold de EAR baseado nos seus olhos:
- Mantenha os olhos ABERTOS normalmente por 10 segundos
- O threshold será ajustado automaticamente

## Troubleshooting

### Não consigo ativar o alarme
- Verifique se o PERCLOS está aumentando (feche os olhos)
- Certifique-se de que a duração chegou a 3s
- O valor de PERCLOS ficará em vermelho quando próximo do threshold

### Não ouço o beep
1. Verifique o volume do Windows
2. Execute `python test_beep.py` para teste isolado
3. Procure por "🚨 ALERTA!" no console - se aparecer, o beep foi executado

### PERCLOS não sobe
- Certifique-se de que seu rosto está sendo detectado (STATE != "NO FACE")
- Feche os olhos completamente
- Verifique se o EAR está abaixo do threshold quando você fecha os olhos

## Ajustes Finos

Para tornar o alarme mais/menos sensível, edite `src/drowsy_driver/config.py`:

```python
@dataclass
class MetricsConfig:
    perclos_threshold: float = 0.50  # Diminua para mais sensível (ex: 0.30)
    persistence_seconds: int = 3     # Diminua para alarme mais rápido (ex: 2)
```

Para alarmes mais frequentes:
```python
@dataclass
class AlertConfig:
    cooldown_seconds: int = 3  # Diminua para menos tempo entre alarmes
```
