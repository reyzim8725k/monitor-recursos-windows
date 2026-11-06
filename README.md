# Monitor de Recursos do PC

Aplicativo Windows leve e gratuito para acompanhar, em tempo real, a memória RAM e o armazenamento do computador.

![Windows](https://img.shields.io/badge/Windows-10%2B-0078D6?logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Licença](https://img.shields.io/badge/licença-MIT-22c55e)

## Download

Baixe a versão mais recente na página de **[Releases](../../releases/latest)**.

> O arquivo recomendado é `MonitorRecursos.exe`. Não é necessário instalar o Python para executar a versão compilada.

## O que ele mostra

- **RAM:** memória total, memória em uso, memória livre e percentual de utilização;
- **Armazenamento principal:** capacidade total, espaço usado e espaço livre do disco do Windows;
- **Armazenamento temporário:** tamanho dos arquivos presentes na pasta temporária e espaço livre no volume onde ela está localizada;
- atualização automática a cada 2 segundos;
- interface em português, simples e sem anúncios;
- funcionamento local, sem envio de informações para a internet.

## Captura de tela

A interface apresenta cartões separados para RAM, armazenamento principal e armazenamento temporário, com barras de utilização e valores atualizados automaticamente.

## Como executar

1. Acesse **[Releases](../../releases/latest)**.
2. Baixe `MonitorRecursos.exe`.
3. Abra o arquivo no Windows.
4. Caso o Windows SmartScreen exiba um aviso para um aplicativo novo, confira se o arquivo foi baixado desta página e escolha **Mais informações → Executar assim mesmo**.

## Executar a partir do código-fonte

Requer Windows e Python 3.10 ou mais recente.

```powershell
python monitor_recursos.py
```

Para criar o executável manualmente, dê duplo clique em `GERAR_EXE.bat` ou execute:

```powershell
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name MonitorRecursos monitor_recursos.py
```

O resultado será salvo em `dist/MonitorRecursos.exe`.

## Privacidade

O aplicativo apenas consulta informações do próprio computador usando as APIs locais do Windows. Nenhum dado é enviado ou armazenado em serviços externos.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE).

---

Feito para oferecer uma visão rápida e clara dos recursos do computador, sem complicação.
