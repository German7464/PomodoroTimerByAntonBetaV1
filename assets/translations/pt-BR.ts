<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="pt_BR">
  <context>
    <name>PomodoroTimer</name>
    <message>
      <source>action.apply</source>
      <translation>Aplicar</translation>
    </message>
    <message>
      <source>action.cancel</source>
      <translation>Cancelar</translation>
    </message>
    <message>
      <source>action.choose</source>
      <translation>Escolher</translation>
    </message>
    <message>
      <source>action.close</source>
      <translation>Fechar</translation>
    </message>
    <message>
      <source>action.continue</source>
      <translation>Continuar</translation>
    </message>
    <message>
      <source>action.continue_next_period</source>
      <translation>Continue e comece o próximo período</translation>
    </message>
    <message>
      <source>action.open</source>
      <translation>Abrir</translation>
    </message>
    <message>
      <source>action.open_main_window</source>
      <translation>Abrir janela principal</translation>
    </message>
    <message>
      <source>action.pause</source>
      <translation>Pausa</translation>
    </message>
    <message>
      <source>action.preview</source>
      <translation>Pré-visualizar</translation>
    </message>
    <message>
      <source>action.refresh</source>
      <translation>Atualizar</translation>
    </message>
    <message>
      <source>action.reset</source>
      <translation>Redefinir</translation>
    </message>
    <message>
      <source>action.show</source>
      <translation>Mostrar</translation>
    </message>
    <message>
      <source>action.skip</source>
      <translation>Pular</translation>
    </message>
    <message>
      <source>action.start</source>
      <translation>Iniciar</translation>
    </message>
    <message>
      <source>dialog.color.choose</source>
      <translation>Escolha uma cor</translation>
    </message>
    <message>
      <source>dialog.color.invalid_hex</source>
      <translation>Corrija os valores: o formato #RRGGBB é obrigatório.</translation>
    </message>
    <message>
      <source>dialog.color.title</source>
      <translation>Cor</translation>
    </message>
    <message>
      <source>error.autostart.python_unavailable</source>
      <translation>A inicialização automática está disponível apenas no EXE empacotado. Não pode ser habilitado ao executar em Python.</translation>
    </message>
    <message>
      <source>error.data.portable_fallback</source>
      <translation>Os dados não puderam ser gravados ao lado do aplicativo. As configurações serão armazenadas temporariamente na sua pasta de usuário. Para o modo portátil, mova o aplicativo para uma pasta gravável.</translation>
    </message>
    <message>
      <source>error.data.portable_title</source>
      <translation>Modo portátil</translation>
    </message>
    <message>
      <source>error.data.unavailable</source>
      <translation>A pasta de configurações do aplicativo não pôde ser criada.</translation>
    </message>
    <message>
      <source>error.widget.hide</source>
      <translation>Não foi possível ocultar o widget: {error}</translation>
    </message>
    <message>
      <source>error.widget.show</source>
      <translation>Não foi possível mostrar o widget: {error}</translation>
    </message>
    <message>
      <source>error.widget.state_mismatch</source>
      <translation>a janela não entrou no estado solicitado</translation>
    </message>
    <message>
      <source>help.content</source>
      <translation>#Temporizador Pomodoro

## Início rápido

Escolha as durações em Configurações, abra o Cronômetro e selecione **Iniciar**. Use o botão na parte superior para alternar entre o modo claro e escuro instantaneamente. As configurações binárias usam opções; ações regulares permanecem botões.

## Controles de temporizador

- **Início** inicia o período atual.
- **Pausar/Continuar** pausa e retoma um período regular.
- **Pular período** passa para o próximo modo sem registrar a duração.
- **Reset** retorna ao Trabalho parado e registra uma reinicialização nas Estatísticas.
- **Continuar e iniciar o próximo período** aparece para uma transição manual, registra a ultrapassagem uma vez e inicia o próximo período imediatamente.

Com transições automáticas, o próximo período começa imediatamente e nenhuma ultrapassagem é contada. Com transições manuais, o aplicativo mostra **Excesso de trabalho**, **Excesso de intervalo curto** ou **Excesso de intervalo longo** e tempo prefixado com `+`. Iniciar, pausar, pular e redefinir permanecem desativados durante uma ultrapassagem para que nenhum tempo seja perdido.

## Aparência e acessibilidade

Os temas Comet, Aurora, Warm e Custom têm modos claro e escuro. O editor de tema personalizado armazena os modos separadamente, valida `#RRGGBB` e avisa quando o contraste está abaixo de 4,5:1. Cancelar restaura as cores salvas; reset restaura a paleta Comet segura.

A interface do Qt Widgets segue o dimensionamento do Windows/Qt e suporta o foco do teclado. Os switches funcionam com o mouse, `Space` ou `Enter`; seu estado é transmitido pela posição, cor e texto ON/OFF. Os botões de comando também usam `Espaço` ou `Enter`, fornecem um breve feedback ao pressionar e mostram um contorno de alto contraste apenas durante a navegação pelo teclado. Quando o movimento está desativado, uma mudança imediata de cor substitui a animação.

Na primeira inicialização, a janela principal utiliza cerca de 80% da tela disponível. Ele lembra seu tamanho e posição e retorna a um monitor visível após alterações na resolução. Em larguras médias e estreitas, a navegação se reduz a ícones com dicas de ferramentas, quebra de grupos de botões e rolagens de configurações sem cortar ações fixadas.

O modo escuro estiliza a janela de visualização e o menu da bandeja e solicita uma barra de título nativa escura quando o Windows DWM oferece suporte. O ícone original do tomate e do cronômetro é usado para janelas, barra de tarefas, bandeja e EXE empacotado.

## Indicação de ultrapassagem

Escolha pulso, dígitos ampliados, sinalizadores, borda acentuada, indicador de onda ou nenhuma animação. Mudanças de cor, escopo, velocidade, intensidade e três cores são configuradas de forma independente. A visualização não modifica o cronômetro, as estatísticas, as notificações ou a opacidade.

A janela principal e o widget recebem o mesmo quadro de efeito. Continuar ou sair restaura cores e tamanhos regulares imediatamente. Com o movimento desativado, a indicação de acesso estático, o nome do estado e o sinal `+` permanecem.

## Widget flutuante

A opção **Mostrar widget** na página Timer mostra e oculta a mesma janela. Sete layouts estão disponíveis: Mínimo, Compacto, Expandido, Micro, Linha, Anel e Placar. Todos usam o mesmo `TimerEngine`.

Tipo, tamanho e posição são armazenados separadamente para cada layout. O redimensionamento manual cria um tamanho personalizado. A opacidade varia de 5 a 100%; durante uma saturação, o widget pode ficar temporariamente totalmente opaco e depois retornar ao valor exato salvo.

Na visualização expandida, uma barra de ação estreita envolve ações inteiras. Continuar nunca é abreviado. Na largura mínima, apenas Open pode se tornar um ícone com uma dica de ferramenta; as ações restantes passam para a próxima linha.

## Notificações, estatísticas e bandeja

Uma notificação de transição automática pode ser fechada. Uma notificação manual inclui Continuar; seu botão Fechar descarta apenas a janela e não perde tempo excedente. O mesmo comando permanece disponível na janela principal e no widget.

As estatísticas separam o trabalho regular, os intervalos regulares e três tipos de sobrecarga para hoje e para sempre. Fechar a janela principal pode minimizar o aplicativo na bandeja. Uma saída completa normal economiza tempo de ultrapassagem acumulado.

Uma instância de aplicativo é executada por usuário do Windows. Uma segunda inicialização mostra uma mensagem do sistema sem criar outra interface.</translation>
    </message>
    <message>
      <source>help.subtitle</source>
      <translation>Recursos e comportamento seguro do aplicativo.</translation>
    </message>
    <message>
      <source>help.title</source>
      <translation>Ajuda</translation>
    </message>
    <message>
      <source>main.brand_subtitle</source>
      <translation>Um ritmo de trabalho calmo</translation>
    </message>
    <message>
      <source>nav.help</source>
      <translation>Ajuda</translation>
    </message>
    <message>
      <source>nav.settings</source>
      <translation>Configurações</translation>
    </message>
    <message>
      <source>nav.statistics</source>
      <translation>Estatísticas</translation>
    </message>
    <message>
      <source>nav.timer</source>
      <translation>Temporizador</translation>
    </message>
    <message>
      <source>notification.auto_transition</source>
      <translation>{completed}

O próximo período já começou: {next_period}.</translation>
    </message>
    <message>
      <source>notification.completed.long_break</source>
      <translation>Pausa longa concluída.</translation>
    </message>
    <message>
      <source>notification.completed.short_break</source>
      <translation>Pausa curta concluída.</translation>
    </message>
    <message>
      <source>notification.completed.work</source>
      <translation>Período de trabalho concluído.</translation>
    </message>
    <message>
      <source>notification.default.long_break_end</source>
      <translation>Pausa longa concluída. É hora de iniciar um novo período de trabalho.</translation>
    </message>
    <message>
      <source>notification.default.short_break_end</source>
      <translation>Pausa curta concluída. Hora de voltar ao trabalho.</translation>
    </message>
    <message>
      <source>notification.default.work_end</source>
      <translation>Período de trabalho concluído. Hora de fazer uma pausa.</translation>
    </message>
    <message>
      <source>notification.manual_transition</source>
      <translation>{completed}

Selecione Continuar para iniciar {next_period}.</translation>
    </message>
    <message>
      <source>overrun.effect.beacons</source>
      <translation>Sinalizadores</translation>
    </message>
    <message>
      <source>overrun.effect.border</source>
      <translation>Borda de destaque</translation>
    </message>
    <message>
      <source>overrun.effect.none</source>
      <translation>Sem animação</translation>
    </message>
    <message>
      <source>overrun.effect.pulse</source>
      <translation>Pulso</translation>
    </message>
    <message>
      <source>overrun.effect.scale</source>
      <translation>Ampliar dígitos</translation>
    </message>
    <message>
      <source>overrun.effect.wave</source>
      <translation>Indicador de onda</translation>
    </message>
    <message>
      <source>overrun.intensity.medium</source>
      <translation>Médio</translation>
    </message>
    <message>
      <source>overrun.intensity.strong</source>
      <translation>Forte</translation>
    </message>
    <message>
      <source>overrun.intensity.weak</source>
      <translation>Sutil</translation>
    </message>
    <message>
      <source>overrun.scope.both</source>
      <translation>Dígitos e cartão do temporizador</translation>
    </message>
    <message>
      <source>overrun.scope.card</source>
      <translation>Cartão do temporizador</translation>
    </message>
    <message>
      <source>overrun.scope.digits</source>
      <translation>Apenas dígitos do temporizador</translation>
    </message>
    <message>
      <source>overrun.speed.fast</source>
      <translation>Rápido</translation>
    </message>
    <message>
      <source>overrun.speed.normal</source>
      <translation>Normal</translation>
    </message>
    <message>
      <source>overrun.speed.slow</source>
      <translation>Lento</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode</source>
      <translation>Modo escuro</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode.description</source>
      <translation>OFF — modo claro, ON — modo escuro.</translation>
    </message>
    <message>
      <source>settings.appearance.edit_colors</source>
      <translation>Personalize cores</translation>
    </message>
    <message>
      <source>settings.appearance.editor_unavailable</source>
      <translation>O editor não está disponível nesta janela.</translation>
    </message>
    <message>
      <source>settings.appearance.language</source>
      <translation>Idioma da interface</translation>
    </message>
    <message>
      <source>settings.appearance.subtitle</source>
      <translation>Paletas completas atualizam cada janela aberta sem reiniciar.</translation>
    </message>
    <message>
      <source>settings.appearance.title</source>
      <translation>Aparência</translation>
    </message>
    <message>
      <source>settings.logic.long_break_interval</source>
      <translation>Períodos de trabalho antes de uma longa pausa</translation>
    </message>
    <message>
      <source>settings.logic.subtitle</source>
      <translation>A ordem de trabalho, pausas curtas e pausas longas.</translation>
    </message>
    <message>
      <source>settings.logic.title</source>
      <translation>Comportamento do temporizador</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break</source>
      <translation>Use pausas longas</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break.description</source>
      <translation>Após o número especificado de períodos de trabalho.</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition</source>
      <translation>Transição automática</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition.description</source>
      <translation>ON — o próximo período começa imediatamente; DESLIGADO — o tempo excedente é contado.</translation>
    </message>
    <message>
      <source>settings.notifications.enabled</source>
      <translation>Notificações</translation>
    </message>
    <message>
      <source>settings.notifications.long_break_end</source>
      <translation>Fim da pausa longa</translation>
    </message>
    <message>
      <source>settings.notifications.short_break_end</source>
      <translation>Fim da pausa curta</translation>
    </message>
    <message>
      <source>settings.notifications.sound</source>
      <translation>Som de notificação</translation>
    </message>
    <message>
      <source>settings.notifications.subtitle</source>
      <translation>Uma transição manual sempre pode ser concluída na janela principal ou widget.</translation>
    </message>
    <message>
      <source>settings.notifications.title</source>
      <translation>Notificações</translation>
    </message>
    <message>
      <source>settings.notifications.work_end</source>
      <translation>Conclusão do trabalho</translation>
    </message>
    <message>
      <source>settings.overrun.allow_motion</source>
      <translation>Permitir movimento de efeito</translation>
    </message>
    <message>
      <source>settings.overrun.change_color</source>
      <translation>Alterar a cor do temporizador</translation>
    </message>
    <message>
      <source>settings.overrun.color_dialog</source>
      <translation>Cor de superação</translation>
    </message>
    <message>
      <source>settings.overrun.effect</source>
      <translation>Efeito principal</translation>
    </message>
    <message>
      <source>settings.overrun.intensity</source>
      <translation>Intensidade</translation>
    </message>
    <message>
      <source>settings.overrun.invalid_colors</source>
      <translation>As cores inválidas foram substituídas por valores do tema ativo.</translation>
    </message>
    <message>
      <source>settings.overrun.opaque_widget</source>
      <translation>Torne o widget opaco durante a saturação</translation>
    </message>
    <message>
      <source>settings.overrun.scope</source>
      <translation>Área de mudança de cor</translation>
    </message>
    <message>
      <source>settings.overrun.separate_colors</source>
      <translation>Cores separadas</translation>
    </message>
    <message>
      <source>settings.overrun.speed</source>
      <translation>Velocidade</translation>
    </message>
    <message>
      <source>settings.overrun.subtitle</source>
      <translation>Um quadro compartilhado é aplicado à janela principal e ao widget aberto.</translation>
    </message>
    <message>
      <source>settings.overrun.title</source>
      <translation>Indicação de tempo excedido</translation>
    </message>
    <message>
      <source>settings.overrun.use_theme_color</source>
      <translation>Use a cor do tema</translation>
    </message>
    <message>
      <source>settings.profiles.apply</source>
      <translation>Aplicar perfil</translation>
    </message>
    <message>
      <source>settings.profiles.default_cannot_delete</source>
      <translation>O perfil padrão não pode ser excluído.</translation>
    </message>
    <message>
      <source>settings.profiles.default_name</source>
      <translation>Padrão</translation>
    </message>
    <message>
      <source>settings.profiles.defaults</source>
      <translation>Configurações padrão</translation>
    </message>
    <message>
      <source>settings.profiles.delete</source>
      <translation>Excluir perfil</translation>
    </message>
    <message>
      <source>settings.profiles.delete_confirmation</source>
      <translation>Excluir perfil “{profile_name}”?</translation>
    </message>
    <message>
      <source>settings.profiles.delete_title</source>
      <translation>Excluir perfil</translation>
    </message>
    <message>
      <source>settings.profiles.dialog_title</source>
      <translation>Perfil</translation>
    </message>
    <message>
      <source>settings.profiles.enter_name</source>
      <translation>Insira um nome de perfil.</translation>
    </message>
    <message>
      <source>settings.profiles.name_placeholder</source>
      <translation>Nome do perfil</translation>
    </message>
    <message>
      <source>settings.profiles.restore_personal</source>
      <translation>Restaurar minhas configurações</translation>
    </message>
    <message>
      <source>settings.profiles.save</source>
      <translation>Salvar perfil</translation>
    </message>
    <message>
      <source>settings.profiles.select_profile</source>
      <translation>Selecione um perfil da lista.</translation>
    </message>
    <message>
      <source>settings.profiles.subtitle</source>
      <translation>Salve conjuntos de durações, opções de aparência e configurações de widget.</translation>
    </message>
    <message>
      <source>settings.profiles.title</source>
      <translation>Perfis</translation>
    </message>
    <message>
      <source>settings.save</source>
      <translation>Salvar configurações</translation>
    </message>
    <message>
      <source>settings.section.appearance</source>
      <translation>Aparência</translation>
    </message>
    <message>
      <source>settings.section.logic</source>
      <translation>Comportamento do temporizador</translation>
    </message>
    <message>
      <source>settings.section.notifications</source>
      <translation>Notificações</translation>
    </message>
    <message>
      <source>settings.section.overrun</source>
      <translation>Superação</translation>
    </message>
    <message>
      <source>settings.section.profiles</source>
      <translation>Perfis</translation>
    </message>
    <message>
      <source>settings.section.time</source>
      <translation>Tempo</translation>
    </message>
    <message>
      <source>settings.section.tray</source>
      <translation>Bandeja e inicialização automática</translation>
    </message>
    <message>
      <source>settings.section.widget</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.subtitle</source>
      <translation>As alterações de tema e widget são aplicadas imediatamente; outras alterações se aplicam após salvar.</translation>
    </message>
    <message>
      <source>settings.time.format</source>
      <translation>Formato de hora</translation>
    </message>
    <message>
      <source>settings.time.long_break_minutes</source>
      <translation>Pausa longa, minutos</translation>
    </message>
    <message>
      <source>settings.time.short_break_minutes</source>
      <translation>Pausa curta, minutos</translation>
    </message>
    <message>
      <source>settings.time.subtitle</source>
      <translation>As durações são aplicadas com segurança quando você salva.</translation>
    </message>
    <message>
      <source>settings.time.title</source>
      <translation>Tempo</translation>
    </message>
    <message>
      <source>settings.time.work_minutes</source>
      <translation>Trabalho, minutos</translation>
    </message>
    <message>
      <source>settings.title</source>
      <translation>Configurações</translation>
    </message>
    <message>
      <source>settings.tray.autostart</source>
      <translation>Comece com o Windows</translation>
    </message>
    <message>
      <source>settings.tray.autostart_current</source>
      <translation>A inicialização automática está habilitada e aponta para a pasta atual do aplicativo.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_disabled</source>
      <translation>A inicialização automática está desabilitada.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_python</source>
      <translation>Executando em Python: a inicialização automática pode ser habilitada na versão EXE.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_stale</source>
      <translation>O caminho de inicialização automática está desatualizado. Atualize-o após mover o aplicativo.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_title</source>
      <translation>Início automático</translation>
    </message>
    <message>
      <source>settings.tray.close_to_tray</source>
      <translation>Minimizar para a bandeja ao fechar</translation>
    </message>
    <message>
      <source>settings.tray.minimize_on_start</source>
      <translation>Minimize o aplicativo após o lançamento</translation>
    </message>
    <message>
      <source>settings.tray.subtitle</source>
      <translation>A bandeja do sistema é executada no thread compartilhado da GUI do Qt.</translation>
    </message>
    <message>
      <source>settings.tray.title</source>
      <translation>Bandeja e inicialização automática</translation>
    </message>
    <message>
      <source>settings.tray.update_autostart</source>
      <translation>Atualizar caminho de inicialização automática</translation>
    </message>
    <message>
      <source>settings.widget.always_on_top</source>
      <translation>Sempre no topo</translation>
    </message>
    <message>
      <source>settings.widget.dialog_title</source>
      <translation>Widget</translation>
    </message>
    <message>
      <source>settings.widget.opacity</source>
      <translation>Opacidade do widget</translation>
    </message>
    <message>
      <source>settings.widget.opacity.description</source>
      <translation>Valores mais baixos tornam o widget mais transparente. Mínimo — 5%.</translation>
    </message>
    <message>
      <source>settings.widget.position_reset</source>
      <translation>A posição do tipo atual foi redefinida.</translation>
    </message>
    <message>
      <source>settings.widget.reset_position</source>
      <translation>Redefinir posição para o tipo atual</translation>
    </message>
    <message>
      <source>settings.widget.size</source>
      <translation>Tamanho</translation>
    </message>
    <message>
      <source>settings.widget.subtitle</source>
      <translation>A visibilidade é controlada pelo interruptor na página do Temporizador.</translation>
    </message>
    <message>
      <source>settings.widget.title</source>
      <translation>Widget flutuante</translation>
    </message>
    <message>
      <source>settings.widget.type</source>
      <translation>Tipo de widget</translation>
    </message>
    <message>
      <source>startup.already_running</source>
      <translation>O Pomodoro Timer está iniciando ou já em execução. Aguarde a janela abrir ou use o aplicativo que já está aberto.</translation>
    </message>
    <message>
      <source>startup.lock.already_running</source>
      <translation>Outra instância do aplicativo já está em execução.</translation>
    </message>
    <message>
      <source>startup.lock.create_failed</source>
      <translation>Não foi possível criar o bloqueio do sistema (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.release_failed</source>
      <translation>Não foi possível liberar o bloqueio do sistema (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.secondary_close_failed</source>
      <translation>Outra instância já está em execução, mas seu identificador secundário não pôde ser fechado (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.unsupported</source>
      <translation>O bloqueio do sistema de instância única tem suporte apenas no Windows.</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_cycles</source>
      <translation>
        <numerusform>Ciclo completo</numerusform>
        <numerusform>Ciclos completos</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_long_breaks</source>
      <translation>
        <numerusform>Pausa longa</numerusform>
        <numerusform>Pausas longas</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_short_breaks</source>
      <translation>
        <numerusform>Pausa curta</numerusform>
        <numerusform>Pausas curtas</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_work_periods</source>
      <translation>
        <numerusform>Período de trabalho</numerusform>
        <numerusform>Períodos de trabalho</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.long_break_overrun</source>
      <translation>Pausa longa além do limite</translation>
    </message>
    <message>
      <source>stats.metric.overwork_time</source>
      <translation>Trabalho além do tempo previsto</translation>
    </message>
    <message>
      <source>stats.metric.rest_time</source>
      <translation>Tempo de intervalo</translation>
    </message>
    <message>
      <source>stats.metric.short_break_overrun</source>
      <translation>Pausa curta além do limite</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.skipped_periods</source>
      <translation>
        <numerusform>Período ignorado</numerusform>
        <numerusform>Períodos ignorados</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.timer_resets</source>
      <translation>
        <numerusform>Reinicialização do temporizador</numerusform>
        <numerusform>Reinicializações do temporizador</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.work_time</source>
      <translation>Tempo de trabalho</translation>
    </message>
    <message>
      <source>stats.period.all_time</source>
      <translation>Todo o tempo</translation>
    </message>
    <message>
      <source>stats.period.today</source>
      <translation>Hoje</translation>
    </message>
    <message>
      <source>stats.reset.action</source>
      <translation>Redefinir estatísticas</translation>
    </message>
    <message>
      <source>stats.reset.confirmation</source>
      <translation>Tem certeza de que deseja excluir todas as estatísticas?</translation>
    </message>
    <message>
      <source>stats.reset.title</source>
      <translation>Redefinir estatísticas</translation>
    </message>
    <message>
      <source>stats.subtitle</source>
      <translation>O tempo normal e os excessos são rastreados separadamente.</translation>
    </message>
    <message>
      <source>stats.title</source>
      <translation>Estatísticas</translation>
    </message>
    <message>
      <source>theme.appearance.dark</source>
      <translation>Escuro</translation>
    </message>
    <message>
      <source>theme.appearance.light</source>
      <translation>Claro</translation>
    </message>
    <message>
      <source>theme.contrast.accent</source>
      <translation>Texto acentuado/acento</translation>
    </message>
    <message>
      <source>theme.contrast.button</source>
      <translation>Texto/botão do botão</translation>
    </message>
    <message>
      <source>theme.contrast.long_break</source>
      <translation>Pausa longa/cartão</translation>
    </message>
    <message>
      <source>theme.contrast.long_break_overrun</source>
      <translation>Pausa longa além do limite / cartão</translation>
    </message>
    <message>
      <source>theme.contrast.overwork</source>
      <translation>Trabalho além do tempo / cartão</translation>
    </message>
    <message>
      <source>theme.contrast.primary_card</source>
      <translation>Texto/cartão principal</translation>
    </message>
    <message>
      <source>theme.contrast.secondary_card</source>
      <translation>Texto/cartão secundário</translation>
    </message>
    <message>
      <source>theme.contrast.short_break</source>
      <translation>Pausa curta / cartão</translation>
    </message>
    <message>
      <source>theme.contrast.short_break_overrun</source>
      <translation>Pausa curta além do limite / cartão</translation>
    </message>
    <message>
      <source>theme.contrast.work</source>
      <translation>Trabalho/cartão</translation>
    </message>
    <message>
      <source>theme.description.aurora</source>
      <translation>Acentos legais em azul e violeta</translation>
    </message>
    <message>
      <source>theme.description.comet</source>
      <translation>Paleta neutra calma</translation>
    </message>
    <message>
      <source>theme.description.custom</source>
      <translation>Suas paletas claras e escuras independentes</translation>
    </message>
    <message>
      <source>theme.description.warm</source>
      <translation>Superfícies arenosas macias e quentes</translation>
    </message>
    <message>
      <source>theme.name.aurora</source>
      <translation>aurora</translation>
    </message>
    <message>
      <source>theme.name.comet</source>
      <translation>Cometa</translation>
    </message>
    <message>
      <source>theme.name.custom</source>
      <translation>Personalizado</translation>
    </message>
    <message>
      <source>theme.name.warm</source>
      <translation>Esquentar</translation>
    </message>
    <message>
      <source>theme_editor.color.accent</source>
      <translation>Sotaque</translation>
    </message>
    <message>
      <source>theme_editor.color.accent_hover</source>
      <translation>Passe o mouse</translation>
    </message>
    <message>
      <source>theme_editor.color.background</source>
      <translation>Antecedentes principais</translation>
    </message>
    <message>
      <source>theme_editor.color.border</source>
      <translation>Fronteiras</translation>
    </message>
    <message>
      <source>theme_editor.color.button_background</source>
      <translation>Cor do botão</translation>
    </message>
    <message>
      <source>theme_editor.color.button_text</source>
      <translation>Texto do botão</translation>
    </message>
    <message>
      <source>theme_editor.color.card_background</source>
      <translation>Fundo do cartão</translation>
    </message>
    <message>
      <source>theme_editor.color.disabled</source>
      <translation>Elementos desativados</translation>
    </message>
    <message>
      <source>theme_editor.color.error</source>
      <translation>Erro</translation>
    </message>
    <message>
      <source>theme_editor.color.focus</source>
      <translation>Foco</translation>
    </message>
    <message>
      <source>theme_editor.color.on_accent</source>
      <translation>Texto do botão de destaque</translation>
    </message>
    <message>
      <source>theme_editor.color.secondary_background</source>
      <translation>Antecedentes secundários</translation>
    </message>
    <message>
      <source>theme_editor.color.success</source>
      <translation>Sucesso</translation>
    </message>
    <message>
      <source>theme_editor.color.text_primary</source>
      <translation>Texto principal</translation>
    </message>
    <message>
      <source>theme_editor.color.text_secondary</source>
      <translation>Texto secundário</translation>
    </message>
    <message>
      <source>theme_editor.color.warning</source>
      <translation>Aviso</translation>
    </message>
    <message>
      <source>theme_editor.contrast.ok</source>
      <translation>Verificação de contraste: as principais combinações atendem à diretriz 4,5:1.</translation>
    </message>
    <message numerus="yes">
      <source>theme_editor.contrast.warning</source>
      <translation>
        <numerusform>Verificação de contraste: a combinação {count} está abaixo de 4,5:1. A confirmação será necessária no momento da inscrição.</numerusform>
        <numerusform>Verificação de contraste: as combinações {count} estão abaixo de 4,5:1. A confirmação será necessária no momento da inscrição.</numerusform>
      </translation>
    </message>
    <message>
      <source>theme_editor.create_copy</source>
      <translation>Criar cópia</translation>
    </message>
    <message>
      <source>theme_editor.create_from</source>
      <translation>Criar a partir de</translation>
    </message>
    <message>
      <source>theme_editor.editing_mode</source>
      <translation>Modo sendo editado</translation>
    </message>
    <message>
      <source>theme_editor.group.service_states</source>
      <translation>Cores de status</translation>
    </message>
    <message>
      <source>theme_editor.group.surfaces</source>
      <translation>Superfícies</translation>
    </message>
    <message>
      <source>theme_editor.group.text_controls</source>
      <translation>Texto e controles</translation>
    </message>
    <message>
      <source>theme_editor.group.timer_states</source>
      <translation>Estados do temporizador</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.confirmation</source>
      <translation>Algumas combinações estão abaixo de 4,5:1:

{details}

Salvar mesmo assim?</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.title</source>
      <translation>Baixo contraste</translation>
    </message>
    <message>
      <source>theme_editor.reset.confirmation</source>
      <translation>Redefinir ambos os modos para o tema Cometa seguro?</translation>
    </message>
    <message>
      <source>theme_editor.reset.title</source>
      <translation>Redefinir tema</translation>
    </message>
    <message>
      <source>theme_editor.reset_all</source>
      <translation>Redefinir todo o tema</translation>
    </message>
    <message>
      <source>theme_editor.reset_mode</source>
      <translation>Redefinir modo atual</translation>
    </message>
    <message>
      <source>theme_editor.subtitle</source>
      <translation>Edite os modos claro e escuro de forma independente.</translation>
    </message>
    <message>
      <source>theme_editor.title</source>
      <translation>Tema personalizado</translation>
    </message>
    <message>
      <source>timer.mode.long_break</source>
      <translation>Pausa longa</translation>
    </message>
    <message>
      <source>timer.mode.long_break_overrun</source>
      <translation>Pausa longa além do limite</translation>
    </message>
    <message>
      <source>timer.mode.overwork</source>
      <translation>Trabalho além do tempo previsto</translation>
    </message>
    <message>
      <source>timer.mode.short_break</source>
      <translation>Pausa curta</translation>
    </message>
    <message>
      <source>timer.mode.short_break_overrun</source>
      <translation>Pausa curta além do limite</translation>
    </message>
    <message>
      <source>timer.mode.work</source>
      <translation>Trabalho</translation>
    </message>
    <message>
      <source>timer.overrun.waiting_status</source>
      <translation>Período concluído – o excesso é contado até você continuar</translation>
    </message>
    <message>
      <source>timer.page.subtitle</source>
      <translation>Um cronômetro para a janela principal, notificações e widget.</translation>
    </message>
    <message>
      <source>timer.page.title</source>
      <translation>Sessão de foco</translation>
    </message>
    <message>
      <source>timer.status.accessible_name</source>
      <translation>Estado do temporizador</translation>
    </message>
    <message>
      <source>timer.status.overrun</source>
      <translation>O tempo excedido está sendo contado</translation>
    </message>
    <message>
      <source>timer.status.paused</source>
      <translation>Temporizador pausado</translation>
    </message>
    <message>
      <source>timer.status.running</source>
      <translation>Temporizador em execução</translation>
    </message>
    <message>
      <source>timer.status.stopped</source>
      <translation>Temporizador parado</translation>
    </message>
    <message>
      <source>timer.widget.show</source>
      <translation>Mostrar widget</translation>
    </message>
    <message>
      <source>timer.widget.show.description</source>
      <translation>Posição, tamanho, tipo e opacidade são salvos separadamente.</translation>
    </message>
    <message>
      <source>toggle.accessible_description</source>
      <translation>LIGADO – habilitado, DESLIGADO – desabilitado</translation>
    </message>
    <message>
      <source>toggle.accessible_name</source>
      <translation>Trocar</translation>
    </message>
    <message>
      <source>toggle.off</source>
      <translation>DESLIGADO</translation>
    </message>
    <message>
      <source>toggle.on</source>
      <translation>SOBRE</translation>
    </message>
    <message>
      <source>toggle.state.off</source>
      <translation>DESLIGADO, desativado</translation>
    </message>
    <message>
      <source>toggle.state.on</source>
      <translation>LIGADO, habilitado</translation>
    </message>
    <message>
      <source>tray.exit</source>
      <translation>Sair</translation>
    </message>
    <message>
      <source>tray.hide</source>
      <translation>Ocultar janela</translation>
    </message>
    <message>
      <source>tray.reset</source>
      <translation>Redefinir</translation>
    </message>
    <message>
      <source>tray.show</source>
      <translation>Mostrar janela</translation>
    </message>
    <message>
      <source>tray.start_pause</source>
      <translation>Iniciar/Pausar</translation>
    </message>
    <message numerus="yes">
      <source>widget.completed_work_periods</source>
      <translation>
        <numerusform>Período de trabalho concluído: {count}</numerusform>
        <numerusform>Períodos de trabalho concluídos: {count}</numerusform>
      </translation>
    </message>
    <message>
      <source>widget.size.custom</source>
      <translation>Personalizado</translation>
    </message>
    <message>
      <source>widget.size.large</source>
      <translation>Grande</translation>
    </message>
    <message>
      <source>widget.size.medium</source>
      <translation>Médio</translation>
    </message>
    <message>
      <source>widget.size.small</source>
      <translation>Pequeno</translation>
    </message>
    <message>
      <source>widget.type.compact</source>
      <translation>Compacto</translation>
    </message>
    <message>
      <source>widget.type.compact.description</source>
      <translation>Um cartão compacto clássico com ação primária.</translation>
    </message>
    <message>
      <source>widget.type.expanded</source>
      <translation>Expandido</translation>
    </message>
    <message>
      <source>widget.type.expanded.description</source>
      <translation>Informações do ciclo e o conjunto completo de ações primárias do temporizador.</translation>
    </message>
    <message>
      <source>widget.type.micro</source>
      <translation>Micro</translation>
    </message>
    <message>
      <source>widget.type.micro.description</source>
      <translation>A menor janela: geralmente apenas a hora.</translation>
    </message>
    <message>
      <source>widget.type.minimal</source>
      <translation>Mínimo</translation>
    </message>
    <message>
      <source>widget.type.minimal.description</source>
      <translation>Tempo grande, nome do estado e detalhes mínimos.</translation>
    </message>
    <message>
      <source>widget.type.ring</source>
      <translation>Anel</translation>
    </message>
    <message>
      <source>widget.type.ring.description</source>
      <translation>Tempo dentro de um indicador de período circular.</translation>
    </message>
    <message>
      <source>widget.type.row</source>
      <translation>Linha</translation>
    </message>
    <message>
      <source>widget.type.row.description</source>
      <translation>Uma linha horizontal para a borda da tela.</translation>
    </message>
    <message>
      <source>widget.type.scoreboard</source>
      <translation>Placar</translation>
    </message>
    <message>
      <source>widget.type.scoreboard.description</source>
      <translation>Grandes dígitos monoespaçados em estilo de placar calmo.</translation>
    </message>
    <message>
      <source>widget.window_title</source>
      <translation>Widget Pomodoro</translation>
    </message>
  </context>
  <context>
    <name>QPlatformTheme</name>
    <message>
      <source>OK</source>
      <translation>OK</translation>
    </message>
    <message>
      <source>Save</source>
      <translation>Salvar</translation>
    </message>
    <message>
      <source>Save All</source>
      <translation>Salvar tudo</translation>
    </message>
    <message>
      <source>Open</source>
      <translation>Abrir</translation>
    </message>
    <message>
      <source>&amp;Yes</source>
      <translation>&amp;Sim</translation>
    </message>
    <message>
      <source>Yes to &amp;All</source>
      <translation>Sim para &amp;todos</translation>
    </message>
    <message>
      <source>&amp;No</source>
      <translation>&amp;Não</translation>
    </message>
    <message>
      <source>N&amp;o to All</source>
      <translation>Não para t&amp;odos</translation>
    </message>
    <message>
      <source>Abort</source>
      <translation>Interromper</translation>
    </message>
    <message>
      <source>Retry</source>
      <translation>Tentar novamente</translation>
    </message>
    <message>
      <source>Ignore</source>
      <translation>Ignorar</translation>
    </message>
    <message>
      <source>Close</source>
      <translation>Fechar</translation>
    </message>
    <message>
      <source>Cancel</source>
      <translation>Cancelar</translation>
    </message>
    <message>
      <source>Discard</source>
      <translation>Descartar</translation>
    </message>
    <message>
      <source>Help</source>
      <translation>Ajuda</translation>
    </message>
    <message>
      <source>Apply</source>
      <translation>Aplicar</translation>
    </message>
    <message>
      <source>Reset</source>
      <translation>Redefinir</translation>
    </message>
    <message>
      <source>Restore Defaults</source>
      <translation>Restaurar padrões</translation>
    </message>
  </context>
</TS>
