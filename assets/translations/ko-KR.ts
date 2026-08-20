<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="ko_KR">
  <context>
    <name>PomodoroTimer</name>
    <message>
      <source>action.apply</source>
      <translation>적용</translation>
    </message>
    <message>
      <source>action.cancel</source>
      <translation>취소</translation>
    </message>
    <message>
      <source>action.choose</source>
      <translation>선택</translation>
    </message>
    <message>
      <source>action.close</source>
      <translation>닫다</translation>
    </message>
    <message>
      <source>action.continue</source>
      <translation>계속</translation>
    </message>
    <message>
      <source>action.continue_next_period</source>
      <translation>계속하고 다음 시간 시작</translation>
    </message>
    <message>
      <source>action.open</source>
      <translation>열기</translation>
    </message>
    <message>
      <source>action.open_main_window</source>
      <translation>메인 창 열기</translation>
    </message>
    <message>
      <source>action.pause</source>
      <translation>일시 중지</translation>
    </message>
    <message>
      <source>action.preview</source>
      <translation>미리 보기</translation>
    </message>
    <message>
      <source>action.refresh</source>
      <translation>새로 고침</translation>
    </message>
    <message>
      <source>action.reset</source>
      <translation>초기화</translation>
    </message>
    <message>
      <source>action.show</source>
      <translation>표시</translation>
    </message>
    <message>
      <source>action.skip</source>
      <translation>건너뛰기</translation>
    </message>
    <message>
      <source>action.start</source>
      <translation>시작</translation>
    </message>
    <message>
      <source>dialog.color.choose</source>
      <translation>색상을 선택하세요</translation>
    </message>
    <message>
      <source>dialog.color.invalid_hex</source>
      <translation>값을 수정하세요. #RRGGBB 형식이 필요합니다.</translation>
    </message>
    <message>
      <source>dialog.color.title</source>
      <translation>색상</translation>
    </message>
    <message>
      <source>error.autostart.python_unavailable</source>
      <translation>자동 시작은 패키지된 EXE에서만 사용할 수 있습니다. Python에서 실행할 때는 활성화할 수 없습니다.</translation>
    </message>
    <message>
      <source>error.data.portable_fallback</source>
      <translation>애플리케이션 옆에 데이터를 쓸 수 없습니다. 설정은 일시적으로 사용자 폴더에 저장됩니다. 휴대용 모드의 경우 애플리케이션을 쓰기 가능한 폴더로 이동합니다.</translation>
    </message>
    <message>
      <source>error.data.portable_title</source>
      <translation>휴대용 모드</translation>
    </message>
    <message>
      <source>error.data.unavailable</source>
      <translation>애플리케이션 설정 폴더를 생성할 수 없습니다.</translation>
    </message>
    <message>
      <source>error.widget.hide</source>
      <translation>위젯을 숨길 수 없습니다: {error}</translation>
    </message>
    <message>
      <source>error.widget.show</source>
      <translation>위젯을 표시할 수 없습니다: {error}</translation>
    </message>
    <message>
      <source>error.widget.state_mismatch</source>
      <translation>창이 요청된 상태로 들어가지 않았습니다.</translation>
    </message>
    <message>
      <source>help.content</source>
      <translation># 포모도로 타이머

## 빠른 시작

설정에서 지속 시간을 선택하고 타이머를 연 다음 **시작**을 선택하세요. 상단의 스위치를 사용하면 밝은 모드와 어두운 모드를 즉시 변경할 수 있습니다. 바이너리 설정은 스위치를 사용합니다. 일반 작업은 버튼으로 유지됩니다.

## 타이머 제어

- **시작**은 현재 기간을 시작합니다.
- **일시 중지/계속**은 정기적인 기간을 일시 중지하고 다시 시작합니다.
- **Skip period** 지속시간을 기록하지 않고 다음 모드로 이동합니다.
- **Reset**은 중지된 작업으로 복귀하고 통계에 재설정을 기록합니다.
- **다음 기간 계속 및 시작**은 수동 전환의 경우 나타나며 오버런을 한 번 기록하고 즉시 다음 기간을 시작합니다.

자동 전환을 사용하면 다음 기간이 즉시 시작되고 초과 실행이 계산되지 않습니다. 수동 전환을 사용하면 애플리케이션에 **과도한 작업**, **짧은 중단 오버런** 또는 **긴 중단 오버런**이 표시되고 앞에 '+'가 붙은 시간이 표시됩니다. 오버런 중에는 시작, 일시 중지, 건너뛰기 및 재설정이 비활성화된 상태로 유지되므로 시간이 손실되지 않습니다.

## 모양 및 접근성

Comet, Aurora, Warm 및 Custom 테마에는 각각 밝은 모드와 어두운 모드가 있습니다. 사용자 정의 테마 편집기는 모드를 별도로 저장하고 `#RRGGBB`를 검증하며 대비가 4.5:1 미만일 때 경고합니다. 취소는 저장된 색상을 복원합니다. 재설정은 안전한 Comet 팔레트를 복원합니다.

Qt 위젯 인터페이스는 Windows/Qt 스케일링을 따르며 키보드 포커스를 지원합니다. 스위치는 마우스, `Space` 또는 `Enter`와 함께 작동합니다. 상태는 위치, 색상, ON/OFF 텍스트로 전달됩니다. 명령 버튼은 'Space' 또는 'Enter'도 사용하고 간단한 누르기 피드백을 제공하며 키보드 탐색 중에만 고대비 윤곽선을 표시합니다. 모션이 비활성화되면 즉각적인 색상 변경이 애니메이션을 대체합니다.

처음 실행 시 기본 창은 사용 가능한 화면의 약 80%를 사용합니다. 크기와 위치를 기억하고 해상도가 변경되면 보이는 모니터로 돌아갑니다. 중간 및 좁은 너비에서는 탐색이 도구 설명이 포함된 아이콘으로 축소되고, 버튼 그룹이 줄바꿈되며, 고정된 작업을 자르지 않고 설정이 스크롤됩니다.

어두운 모드는 뷰포트와 트레이 메뉴의 스타일을 지정하고 Windows DWM이 지원할 경우 어두운 기본 제목 표시줄을 요청합니다. 원래 토마토 및 타이머 아이콘은 창, 작업 표시줄, 트레이 및 패키지 EXE에 사용됩니다.

## 오버런 표시

펄스, 확대된 숫자, 신호 비콘, 악센트 테두리, 물결 표시기 또는 애니메이션 없음을 선택하십시오. 색상 변경, 범위, 속도, 강도 및 세 가지 색상이 독립적으로 구성됩니다. 미리보기는 타이머, 통계, 알림 또는 불투명도를 수정하지 않습니다.

기본 창과 위젯은 동일한 효과 프레임을 받습니다. 계속하거나 종료하면 일반 색상과 크기가 즉시 복원됩니다. 모션이 비활성화되면 정적 액세스 가능 표시, 상태 이름 및 '+' 기호가 유지됩니다.

## 플로팅 위젯

타이머 페이지의 **위젯 표시** 스위치는 동일한 창을 표시하거나 숨깁니다. Minimal, Compact, Expanded, Micro, Row, Ring 및 Scoreboard의 7가지 레이아웃을 사용할 수 있습니다. 모두 동일한 `TimerEngine`을 사용합니다.

유형, 크기, 위치는 각 레이아웃마다 별도로 저장됩니다. 수동으로 크기를 조정하면 사용자 정의 크기가 생성됩니다. 불투명도 범위는 5~100%입니다. 오버런 중에 위젯은 일시적으로 완전히 불투명해졌다가 정확한 저장된 값으로 돌아갈 수 있습니다.

확장 보기에서는 좁은 작업 표시줄이 전체 작업을 둘러쌉니다. 계속은 축약되지 않습니다. 최소 너비에서만 Open은 도구 설명이 있는 아이콘이 될 수 있습니다. 나머지 작업은 다음 행으로 래핑됩니다.

## 알림, 통계 및 트레이

자동 전환 알림을 닫을 수 있습니다. 수동 알림에는 계속이 포함됩니다. 닫기 버튼은 창만 닫고 오버런 시간을 잃지 않습니다. 기본 창과 위젯에서는 동일한 명령을 계속 사용할 수 있습니다.

통계는 오늘과 항상에 대한 정규 작업, 정규 휴식, 세 가지 초과 실행 유형을 구분합니다. 메인 창을 닫으면 트레이에 애플리케이션이 최소화될 수 있습니다. 정상적인 완전 종료는 누적된 오버런 시간을 절약합니다.

Windows 사용자당 하나의 애플리케이션 인스턴스가 실행됩니다. 두 번째 실행에서는 다른 인터페이스를 생성하지 않고 시스템 메시지를 표시합니다.</translation>
    </message>
    <message>
      <source>help.subtitle</source>
      <translation>기능 및 안전한 애플리케이션 동작.</translation>
    </message>
    <message>
      <source>help.title</source>
      <translation>돕다</translation>
    </message>
    <message>
      <source>main.brand_subtitle</source>
      <translation>차분한 업무 리듬</translation>
    </message>
    <message>
      <source>nav.help</source>
      <translation>돕다</translation>
    </message>
    <message>
      <source>nav.settings</source>
      <translation>설정</translation>
    </message>
    <message>
      <source>nav.statistics</source>
      <translation>통계</translation>
    </message>
    <message>
      <source>nav.timer</source>
      <translation>시간제 노동자</translation>
    </message>
    <message>
      <source>notification.auto_transition</source>
      <translation>{completed}

        다음 시간이 이미 시작되었습니다: {next_period}.</translation>
    </message>
    <message>
      <source>notification.completed.long_break</source>
      <translation>긴 휴식이 끝났습니다.</translation>
    </message>
    <message>
      <source>notification.completed.short_break</source>
      <translation>짧은 휴식이 완료되었습니다.</translation>
    </message>
    <message>
      <source>notification.completed.work</source>
      <translation>작업 시간이 끝났습니다.</translation>
    </message>
    <message>
      <source>notification.default.long_break_end</source>
      <translation>긴 휴식이 끝났습니다. 새로운 작업 시간을 시작하세요.</translation>
    </message>
    <message>
      <source>notification.default.short_break_end</source>
      <translation>짧은 휴식이 끝났습니다. 작업으로 돌아갈 시간입니다.</translation>
    </message>
    <message>
      <source>notification.default.work_end</source>
      <translation>작업 시간이 끝났습니다. 이제 휴식하세요.</translation>
    </message>
    <message>
      <source>notification.manual_transition</source>
      <translation>{completed}

        “계속”을 선택하여 {next_period}를 시작하세요.</translation>
    </message>
    <message>
      <source>overrun.effect.beacons</source>
      <translation>경고 표시등</translation>
    </message>
    <message>
      <source>overrun.effect.border</source>
      <translation>강조 테두리</translation>
    </message>
    <message>
      <source>overrun.effect.none</source>
      <translation>움직임 없음</translation>
    </message>
    <message>
      <source>overrun.effect.pulse</source>
      <translation>맥동</translation>
    </message>
    <message>
      <source>overrun.effect.scale</source>
      <translation>숫자 확대</translation>
    </message>
    <message>
      <source>overrun.effect.wave</source>
      <translation>물결 표시기</translation>
    </message>
    <message>
      <source>overrun.intensity.medium</source>
      <translation>중간</translation>
    </message>
    <message>
      <source>overrun.intensity.strong</source>
      <translation>강함</translation>
    </message>
    <message>
      <source>overrun.intensity.weak</source>
      <translation>약함</translation>
    </message>
    <message>
      <source>overrun.scope.both</source>
      <translation>숫자 및 타이머 카드</translation>
    </message>
    <message>
      <source>overrun.scope.card</source>
      <translation>타이머 카드</translation>
    </message>
    <message>
      <source>overrun.scope.digits</source>
      <translation>타이머 숫자만</translation>
    </message>
    <message>
      <source>overrun.speed.fast</source>
      <translation>빠른</translation>
    </message>
    <message>
      <source>overrun.speed.normal</source>
      <translation>보통</translation>
    </message>
    <message>
      <source>overrun.speed.slow</source>
      <translation>느린</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode</source>
      <translation>다크 모드</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode.description</source>
      <translation>OFF — 밝은 모드, ON — 어두운 모드.</translation>
    </message>
    <message>
      <source>settings.appearance.edit_colors</source>
      <translation>색상 맞춤설정</translation>
    </message>
    <message>
      <source>settings.appearance.editor_unavailable</source>
      <translation>이 창에서는 편집기를 사용할 수 없습니다.</translation>
    </message>
    <message>
      <source>settings.appearance.language</source>
      <translation>인터페이스 언어</translation>
    </message>
    <message>
      <source>settings.appearance.subtitle</source>
      <translation>전체 팔레트는 다시 시작하지 않고도 열려 있는 모든 창을 업데이트합니다.</translation>
    </message>
    <message>
      <source>settings.appearance.title</source>
      <translation>모습</translation>
    </message>
    <message>
      <source>settings.logic.long_break_interval</source>
      <translation>긴 휴식 전 작업 기간</translation>
    </message>
    <message>
      <source>settings.logic.subtitle</source>
      <translation>작업 순서, 짧은 휴식, 긴 휴식.</translation>
    </message>
    <message>
      <source>settings.logic.title</source>
      <translation>타이머 동작</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break</source>
      <translation>긴 휴식 시간을 활용하세요</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break.description</source>
      <translation>지정된 작업 기간 이후.</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition</source>
      <translation>자동 전환</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition.description</source>
      <translation>ON - 다음 기간이 즉시 시작됩니다. OFF - 오버런 시간이 계산됩니다.</translation>
    </message>
    <message>
      <source>settings.notifications.enabled</source>
      <translation>알림</translation>
    </message>
    <message>
      <source>settings.notifications.long_break_end</source>
      <translation>긴 휴식 완료</translation>
    </message>
    <message>
      <source>settings.notifications.short_break_end</source>
      <translation>짧은 휴식 완료</translation>
    </message>
    <message>
      <source>settings.notifications.sound</source>
      <translation>알림음</translation>
    </message>
    <message>
      <source>settings.notifications.subtitle</source>
      <translation>수동 전환은 언제든지 기본 창이나 위젯에서 완료할 수 있습니다.</translation>
    </message>
    <message>
      <source>settings.notifications.title</source>
      <translation>알림</translation>
    </message>
    <message>
      <source>settings.notifications.work_end</source>
      <translation>작업완료</translation>
    </message>
    <message>
      <source>settings.overrun.allow_motion</source>
      <translation>효과 모션 허용</translation>
    </message>
    <message>
      <source>settings.overrun.change_color</source>
      <translation>타이머 색상 변경</translation>
    </message>
    <message>
      <source>settings.overrun.color_dialog</source>
      <translation>오버런 색상</translation>
    </message>
    <message>
      <source>settings.overrun.effect</source>
      <translation>기본 효과</translation>
    </message>
    <message>
      <source>settings.overrun.intensity</source>
      <translation>강함</translation>
    </message>
    <message>
      <source>settings.overrun.invalid_colors</source>
      <translation>잘못된 색상이 활성 테마의 값으로 대체되었습니다.</translation>
    </message>
    <message>
      <source>settings.overrun.opaque_widget</source>
      <translation>오버런 중에 위젯을 불투명하게 만듭니다.</translation>
    </message>
    <message>
      <source>settings.overrun.scope</source>
      <translation>색상 변경 영역</translation>
    </message>
    <message>
      <source>settings.overrun.separate_colors</source>
      <translation>별도의 색상</translation>
    </message>
    <message>
      <source>settings.overrun.speed</source>
      <translation>속도</translation>
    </message>
    <message>
      <source>settings.overrun.subtitle</source>
      <translation>하나의 공유 프레임이 메인 창과 열린 위젯에 적용됩니다.</translation>
    </message>
    <message>
      <source>settings.overrun.title</source>
      <translation>초과 시간 표시</translation>
    </message>
    <message>
      <source>settings.overrun.use_theme_color</source>
      <translation>테마 색상 사용</translation>
    </message>
    <message>
      <source>settings.profiles.apply</source>
      <translation>프로필 적용</translation>
    </message>
    <message>
      <source>settings.profiles.default_cannot_delete</source>
      <translation>기본 프로필은 삭제할 수 없습니다.</translation>
    </message>
    <message>
      <source>settings.profiles.default_name</source>
      <translation>기본</translation>
    </message>
    <message>
      <source>settings.profiles.defaults</source>
      <translation>기본 설정</translation>
    </message>
    <message>
      <source>settings.profiles.delete</source>
      <translation>프로필 삭제</translation>
    </message>
    <message>
      <source>settings.profiles.delete_confirmation</source>
      <translation>프로필 '{profile_name}'을 삭제하시겠습니까?</translation>
    </message>
    <message>
      <source>settings.profiles.delete_title</source>
      <translation>프로필 삭제</translation>
    </message>
    <message>
      <source>settings.profiles.dialog_title</source>
      <translation>윤곽</translation>
    </message>
    <message>
      <source>settings.profiles.enter_name</source>
      <translation>프로필 이름을 입력하세요.</translation>
    </message>
    <message>
      <source>settings.profiles.name_placeholder</source>
      <translation>프로필 이름</translation>
    </message>
    <message>
      <source>settings.profiles.restore_personal</source>
      <translation>내 설정 복원</translation>
    </message>
    <message>
      <source>settings.profiles.save</source>
      <translation>프로필 저장</translation>
    </message>
    <message>
      <source>settings.profiles.select_profile</source>
      <translation>목록에서 프로필을 선택합니다.</translation>
    </message>
    <message>
      <source>settings.profiles.subtitle</source>
      <translation>지속 시간, 모양 옵션 및 위젯 설정 세트를 저장합니다.</translation>
    </message>
    <message>
      <source>settings.profiles.title</source>
      <translation>프로필</translation>
    </message>
    <message>
      <source>settings.save</source>
      <translation>설정 저장</translation>
    </message>
    <message>
      <source>settings.section.appearance</source>
      <translation>모습</translation>
    </message>
    <message>
      <source>settings.section.logic</source>
      <translation>타이머 동작</translation>
    </message>
    <message>
      <source>settings.section.notifications</source>
      <translation>알림</translation>
    </message>
    <message>
      <source>settings.section.overrun</source>
      <translation>오버런</translation>
    </message>
    <message>
      <source>settings.section.profiles</source>
      <translation>프로필</translation>
    </message>
    <message>
      <source>settings.section.time</source>
      <translation>시간</translation>
    </message>
    <message>
      <source>settings.section.tray</source>
      <translation>트레이 및 자동 시작</translation>
    </message>
    <message>
      <source>settings.section.widget</source>
      <translation>위젯</translation>
    </message>
    <message>
      <source>settings.subtitle</source>
      <translation>테마 및 위젯 변경 사항은 즉시 적용됩니다. 다른 변경사항은 저장 후 적용됩니다.</translation>
    </message>
    <message>
      <source>settings.time.format</source>
      <translation>시간 형식</translation>
    </message>
    <message>
      <source>settings.time.long_break_minutes</source>
      <translation>긴 휴식 시간(분)</translation>
    </message>
    <message>
      <source>settings.time.short_break_minutes</source>
      <translation>짧은 휴식, 분</translation>
    </message>
    <message>
      <source>settings.time.subtitle</source>
      <translation>저장 시 기간은 안전하게 적용됩니다.</translation>
    </message>
    <message>
      <source>settings.time.title</source>
      <translation>시간</translation>
    </message>
    <message>
      <source>settings.time.work_minutes</source>
      <translation>일, 분</translation>
    </message>
    <message>
      <source>settings.title</source>
      <translation>설정</translation>
    </message>
    <message>
      <source>settings.tray.autostart</source>
      <translation>윈도우로 시작하기</translation>
    </message>
    <message>
      <source>settings.tray.autostart_current</source>
      <translation>자동 시작이 활성화되고 애플리케이션의 현재 폴더를 가리킵니다.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_disabled</source>
      <translation>자동 시작이 비활성화되었습니다.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_python</source>
      <translation>Python에서 실행: EXE 버전에서 자동 시작을 활성화할 수 있습니다.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_stale</source>
      <translation>자동 시작 경로가 오래되었습니다. 애플리케이션을 이동한 후 업데이트하세요.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_title</source>
      <translation>자동 시작</translation>
    </message>
    <message>
      <source>settings.tray.close_to_tray</source>
      <translation>닫을 때 트레이로 최소화</translation>
    </message>
    <message>
      <source>settings.tray.minimize_on_start</source>
      <translation>실행 후 애플리케이션 최소화</translation>
    </message>
    <message>
      <source>settings.tray.subtitle</source>
      <translation>시스템 트레이는 공유 Qt GUI 스레드에서 실행됩니다.</translation>
    </message>
    <message>
      <source>settings.tray.title</source>
      <translation>트레이 및 자동 시작</translation>
    </message>
    <message>
      <source>settings.tray.update_autostart</source>
      <translation>자동 시작 경로 업데이트</translation>
    </message>
    <message>
      <source>settings.widget.always_on_top</source>
      <translation>항상 위</translation>
    </message>
    <message>
      <source>settings.widget.dialog_title</source>
      <translation>위젯</translation>
    </message>
    <message>
      <source>settings.widget.opacity</source>
      <translation>위젯 불투명도</translation>
    </message>
    <message>
      <source>settings.widget.opacity.description</source>
      <translation>값이 낮을수록 위젯이 더 투명해집니다. 최소 — 5%.</translation>
    </message>
    <message>
      <source>settings.widget.position_reset</source>
      <translation>현재 유형의 위치가 재설정되었습니다.</translation>
    </message>
    <message>
      <source>settings.widget.reset_position</source>
      <translation>현재 유형의 위치 재설정</translation>
    </message>
    <message>
      <source>settings.widget.size</source>
      <translation>크기</translation>
    </message>
    <message>
      <source>settings.widget.subtitle</source>
      <translation>가시성은 타이머 페이지의 스위치로 제어됩니다.</translation>
    </message>
    <message>
      <source>settings.widget.title</source>
      <translation>플로팅 위젯</translation>
    </message>
    <message>
      <source>settings.widget.type</source>
      <translation>위젯 유형</translation>
    </message>
    <message>
      <source>startup.already_running</source>
      <translation>뽀모도로 타이머가 시작 중이거나 이미 실행 중입니다. 창이 열릴 때까지 기다리거나 이미 열려 있는 애플리케이션을 사용하세요.</translation>
    </message>
    <message>
      <source>startup.lock.already_running</source>
      <translation>다른 애플리케이션 인스턴스가 이미 실행 중입니다.</translation>
    </message>
    <message>
      <source>startup.lock.create_failed</source>
      <translation>시스템 잠금을 생성할 수 없습니다(WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.release_failed</source>
      <translation>시스템 잠금을 해제할 수 없습니다(WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.secondary_close_failed</source>
      <translation>다른 인스턴스가 이미 실행 중이지만 보조 핸들을 닫을 수 없습니다(WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.unsupported</source>
      <translation>단일 인스턴스 시스템 잠금은 Windows에서만 지원됩니다.</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_cycles</source>
      <translation>
        <numerusform>완전한 사이클</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_long_breaks</source>
      <translation>
        <numerusform>긴 휴식</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_short_breaks</source>
      <translation>
        <numerusform>짧은 휴식</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_work_periods</source>
      <translation>
        <numerusform>완료한 작업</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.long_break_overrun</source>
      <translation>긴 휴식 시간 초과</translation>
    </message>
    <message>
      <source>stats.metric.overwork_time</source>
      <translation>연장 작업 시간</translation>
    </message>
    <message>
      <source>stats.metric.rest_time</source>
      <translation>휴식 시간</translation>
    </message>
    <message>
      <source>stats.metric.short_break_overrun</source>
      <translation>짧은 휴식 시간 초과</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.skipped_periods</source>
      <translation>
        <numerusform>건너뛴 기간</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.timer_resets</source>
      <translation>
        <numerusform>타이머 재설정</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.work_time</source>
      <translation>근무 시간</translation>
    </message>
    <message>
      <source>stats.period.all_time</source>
      <translation>모든 시간</translation>
    </message>
    <message>
      <source>stats.period.today</source>
      <translation>오늘</translation>
    </message>
    <message>
      <source>stats.reset.action</source>
      <translation>통계 재설정</translation>
    </message>
    <message>
      <source>stats.reset.confirmation</source>
      <translation>모든 통계를 삭제하시겠습니까?</translation>
    </message>
    <message>
      <source>stats.reset.title</source>
      <translation>통계 재설정</translation>
    </message>
    <message>
      <source>stats.subtitle</source>
      <translation>정규 시간과 오버런은 별도로 추적됩니다.</translation>
    </message>
    <message>
      <source>stats.title</source>
      <translation>통계</translation>
    </message>
    <message>
      <source>theme.appearance.dark</source>
      <translation>어둡게</translation>
    </message>
    <message>
      <source>theme.appearance.light</source>
      <translation>밝게</translation>
    </message>
    <message>
      <source>theme.contrast.accent</source>
      <translation>악센트 텍스트 / 악센트</translation>
    </message>
    <message>
      <source>theme.contrast.button</source>
      <translation>버튼 텍스트 / 버튼</translation>
    </message>
    <message>
      <source>theme.contrast.long_break</source>
      <translation>긴 휴식/카드</translation>
    </message>
    <message>
      <source>theme.contrast.long_break_overrun</source>
      <translation>긴 휴식 시간 초과 / 카드</translation>
    </message>
    <message>
      <source>theme.contrast.overwork</source>
      <translation>연장 작업 / 카드</translation>
    </message>
    <message>
      <source>theme.contrast.primary_card</source>
      <translation>기본 텍스트/카드</translation>
    </message>
    <message>
      <source>theme.contrast.secondary_card</source>
      <translation>보조 텍스트/카드</translation>
    </message>
    <message>
      <source>theme.contrast.short_break</source>
      <translation>짧은 휴식/카드</translation>
    </message>
    <message>
      <source>theme.contrast.short_break_overrun</source>
      <translation>짧은 휴식 시간 초과 / 카드</translation>
    </message>
    <message>
      <source>theme.contrast.work</source>
      <translation>일 / 카드</translation>
    </message>
    <message>
      <source>theme.description.aurora</source>
      <translation>시원한 파란색과 보라색 액센트</translation>
    </message>
    <message>
      <source>theme.description.comet</source>
      <translation>차분한 뉴트럴 팔레트</translation>
    </message>
    <message>
      <source>theme.description.custom</source>
      <translation>독립적인 밝은 팔레트와 어두운 팔레트</translation>
    </message>
    <message>
      <source>theme.description.warm</source>
      <translation>부드러운 모래와 따뜻한 표면</translation>
    </message>
    <message>
      <source>theme.name.aurora</source>
      <translation>오로라</translation>
    </message>
    <message>
      <source>theme.name.comet</source>
      <translation>혜성</translation>
    </message>
    <message>
      <source>theme.name.custom</source>
      <translation>사용자 지정</translation>
    </message>
    <message>
      <source>theme.name.warm</source>
      <translation>따뜻한</translation>
    </message>
    <message>
      <source>theme_editor.color.accent</source>
      <translation>악센트</translation>
    </message>
    <message>
      <source>theme_editor.color.accent_hover</source>
      <translation>호버</translation>
    </message>
    <message>
      <source>theme_editor.color.background</source>
      <translation>주요 배경</translation>
    </message>
    <message>
      <source>theme_editor.color.border</source>
      <translation>테두리</translation>
    </message>
    <message>
      <source>theme_editor.color.button_background</source>
      <translation>버튼 색상</translation>
    </message>
    <message>
      <source>theme_editor.color.button_text</source>
      <translation>버튼 텍스트</translation>
    </message>
    <message>
      <source>theme_editor.color.card_background</source>
      <translation>카드 배경</translation>
    </message>
    <message>
      <source>theme_editor.color.disabled</source>
      <translation>비활성화된 요소</translation>
    </message>
    <message>
      <source>theme_editor.color.error</source>
      <translation>오류</translation>
    </message>
    <message>
      <source>theme_editor.color.focus</source>
      <translation>집중하다</translation>
    </message>
    <message>
      <source>theme_editor.color.on_accent</source>
      <translation>악센트 버튼 텍스트</translation>
    </message>
    <message>
      <source>theme_editor.color.secondary_background</source>
      <translation>보조 배경</translation>
    </message>
    <message>
      <source>theme_editor.color.success</source>
      <translation>성공</translation>
    </message>
    <message>
      <source>theme_editor.color.text_primary</source>
      <translation>기본 텍스트</translation>
    </message>
    <message>
      <source>theme_editor.color.text_secondary</source>
      <translation>보조 텍스트</translation>
    </message>
    <message>
      <source>theme_editor.color.warning</source>
      <translation>경고</translation>
    </message>
    <message>
      <source>theme_editor.contrast.ok</source>
      <translation>대비 확인: 주요 조합은 4.5:1 지침을 충족합니다.</translation>
    </message>
    <message numerus="yes">
      <source>theme_editor.contrast.warning</source>
      <translation>
        <numerusform>대비 확인: {count} 조합은 4.5:1 미만입니다. 신청시 확인이 필요합니다.</numerusform>
      </translation>
    </message>
    <message>
      <source>theme_editor.create_copy</source>
      <translation>사본 만들기</translation>
    </message>
    <message>
      <source>theme_editor.create_from</source>
      <translation>다음에서 생성</translation>
    </message>
    <message>
      <source>theme_editor.editing_mode</source>
      <translation>편집 중인 모드</translation>
    </message>
    <message>
      <source>theme_editor.group.service_states</source>
      <translation>상태 색상</translation>
    </message>
    <message>
      <source>theme_editor.group.surfaces</source>
      <translation>표면</translation>
    </message>
    <message>
      <source>theme_editor.group.text_controls</source>
      <translation>텍스트 및 컨트롤</translation>
    </message>
    <message>
      <source>theme_editor.group.timer_states</source>
      <translation>타이머 상태</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.confirmation</source>
      <translation>일부 조합은 4.5:1 미만입니다.

{details}

저장하시겠습니까?</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.title</source>
      <translation>낮은 대비</translation>
    </message>
    <message>
      <source>theme_editor.reset.confirmation</source>
      <translation>두 모드를 모두 안전한 Comet 테마로 재설정하시겠습니까?</translation>
    </message>
    <message>
      <source>theme_editor.reset.title</source>
      <translation>테마 재설정</translation>
    </message>
    <message>
      <source>theme_editor.reset_all</source>
      <translation>전체 테마 재설정</translation>
    </message>
    <message>
      <source>theme_editor.reset_mode</source>
      <translation>현재 모드 재설정</translation>
    </message>
    <message>
      <source>theme_editor.subtitle</source>
      <translation>밝은 모드와 어두운 모드를 독립적으로 편집합니다.</translation>
    </message>
    <message>
      <source>theme_editor.title</source>
      <translation>맞춤 테마</translation>
    </message>
    <message>
      <source>timer.mode.long_break</source>
      <translation>긴 휴식</translation>
    </message>
    <message>
      <source>timer.mode.long_break_overrun</source>
      <translation>긴 휴식 시간 초과</translation>
    </message>
    <message>
      <source>timer.mode.overwork</source>
      <translation>연장 작업</translation>
    </message>
    <message>
      <source>timer.mode.short_break</source>
      <translation>짧은 휴식</translation>
    </message>
    <message>
      <source>timer.mode.short_break_overrun</source>
      <translation>짧은 휴식 시간 초과</translation>
    </message>
    <message>
      <source>timer.mode.work</source>
      <translation>작업</translation>
    </message>
    <message>
      <source>timer.overrun.waiting_status</source>
      <translation>시간 종료 — 계속할 때까지 초과 시간이 계산됩니다.</translation>
    </message>
    <message>
      <source>timer.page.subtitle</source>
      <translation>기본 창, 알림 및 위젯에 대한 타이머 1개.</translation>
    </message>
    <message>
      <source>timer.page.title</source>
      <translation>포커스 세션</translation>
    </message>
    <message>
      <source>timer.status.accessible_name</source>
      <translation>타이머 상태</translation>
    </message>
    <message>
      <source>timer.status.overrun</source>
      <translation>초과 시간 계산 중</translation>
    </message>
    <message>
      <source>timer.status.paused</source>
      <translation>타이머가 일시중지되었습니다.</translation>
    </message>
    <message>
      <source>timer.status.running</source>
      <translation>타이머 작동 중</translation>
    </message>
    <message>
      <source>timer.status.stopped</source>
      <translation>타이머가 중지되었습니다.</translation>
    </message>
    <message>
      <source>timer.widget.show</source>
      <translation>위젯 표시</translation>
    </message>
    <message>
      <source>timer.widget.show.description</source>
      <translation>위치, 크기, 유형, 불투명도가 별도로 저장됩니다.</translation>
    </message>
    <message>
      <source>toggle.accessible_description</source>
      <translation>ON — 활성화, OFF — 비활성화</translation>
    </message>
    <message>
      <source>toggle.accessible_name</source>
      <translation>스위치</translation>
    </message>
    <message>
      <source>toggle.off</source>
      <translation>끄다</translation>
    </message>
    <message>
      <source>toggle.on</source>
      <translation>에</translation>
    </message>
    <message>
      <source>toggle.state.off</source>
      <translation>꺼짐, 비활성화됨</translation>
    </message>
    <message>
      <source>toggle.state.on</source>
      <translation>켜짐, 활성화됨</translation>
    </message>
    <message>
      <source>tray.exit</source>
      <translation>종료</translation>
    </message>
    <message>
      <source>tray.hide</source>
      <translation>창 숨기기</translation>
    </message>
    <message>
      <source>tray.reset</source>
      <translation>초기화</translation>
    </message>
    <message>
      <source>tray.show</source>
      <translation>창 표시</translation>
    </message>
    <message>
      <source>tray.start_pause</source>
      <translation>시작/일시 중지</translation>
    </message>
    <message numerus="yes">
      <source>widget.completed_work_periods</source>
      <translation>
        <numerusform>완료된 작업 기간: {count}</numerusform>
      </translation>
    </message>
    <message>
      <source>widget.size.custom</source>
      <translation>사용자 지정</translation>
    </message>
    <message>
      <source>widget.size.large</source>
      <translation>크게</translation>
    </message>
    <message>
      <source>widget.size.medium</source>
      <translation>중간</translation>
    </message>
    <message>
      <source>widget.size.small</source>
      <translation>작게</translation>
    </message>
    <message>
      <source>widget.type.compact</source>
      <translation>콤팩트</translation>
    </message>
    <message>
      <source>widget.type.compact.description</source>
      <translation>기본 액션이 포함된 클래식 컴팩트 카드입니다.</translation>
    </message>
    <message>
      <source>widget.type.expanded</source>
      <translation>확장형</translation>
    </message>
    <message>
      <source>widget.type.expanded.description</source>
      <translation>사이클 정보 및 기본 타이머 작업의 전체 세트입니다.</translation>
    </message>
    <message>
      <source>widget.type.micro</source>
      <translation>마이크로</translation>
    </message>
    <message>
      <source>widget.type.micro.description</source>
      <translation>가장 작은 창: 일반적으로 시간만 표시됩니다.</translation>
    </message>
    <message>
      <source>widget.type.minimal</source>
      <translation>최소</translation>
    </message>
    <message>
      <source>widget.type.minimal.description</source>
      <translation>긴 시간, 주 이름, 최소한의 세부정보입니다.</translation>
    </message>
    <message>
      <source>widget.type.ring</source>
      <translation>원형</translation>
    </message>
    <message>
      <source>widget.type.ring.description</source>
      <translation>원형 주기 표시기 내부의 시간입니다.</translation>
    </message>
    <message>
      <source>widget.type.row</source>
      <translation>가로형</translation>
    </message>
    <message>
      <source>widget.type.row.description</source>
      <translation>화면 가장자리의 가로 행입니다.</translation>
    </message>
    <message>
      <source>widget.type.scoreboard</source>
      <translation>점수판</translation>
    </message>
    <message>
      <source>widget.type.scoreboard.description</source>
      <translation>차분한 점수판 스타일의 큰 고정폭 숫자입니다.</translation>
    </message>
    <message>
      <source>widget.window_title</source>
      <translation>뽀모도로 위젯</translation>
    </message>
  </context>
  <context>
    <name>QPlatformTheme</name>
    <message>
      <source>OK</source>
      <translation>확인</translation>
    </message>
    <message>
      <source>Save</source>
      <translation>저장</translation>
    </message>
    <message>
      <source>Save All</source>
      <translation>모두 저장</translation>
    </message>
    <message>
      <source>Open</source>
      <translation>열기</translation>
    </message>
    <message>
      <source>&amp;Yes</source>
      <translation>예(&amp;Y)</translation>
    </message>
    <message>
      <source>Yes to &amp;All</source>
      <translation>모두 예(&amp;A)</translation>
    </message>
    <message>
      <source>&amp;No</source>
      <translation>아니요(&amp;N)</translation>
    </message>
    <message>
      <source>N&amp;o to All</source>
      <translation>모두 아니요(&amp;O)</translation>
    </message>
    <message>
      <source>Abort</source>
      <translation>중단</translation>
    </message>
    <message>
      <source>Retry</source>
      <translation>다시 시도</translation>
    </message>
    <message>
      <source>Ignore</source>
      <translation>무시</translation>
    </message>
    <message>
      <source>Close</source>
      <translation>닫기</translation>
    </message>
    <message>
      <source>Cancel</source>
      <translation>취소</translation>
    </message>
    <message>
      <source>Discard</source>
      <translation>변경 사항 버리기</translation>
    </message>
    <message>
      <source>Help</source>
      <translation>도움말</translation>
    </message>
    <message>
      <source>Apply</source>
      <translation>적용</translation>
    </message>
    <message>
      <source>Reset</source>
      <translation>재설정</translation>
    </message>
    <message>
      <source>Restore Defaults</source>
      <translation>기본값 복원</translation>
    </message>
  </context>
</TS>
