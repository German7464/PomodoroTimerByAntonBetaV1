<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="ar_SA">
  <context>
    <name>PomodoroTimer</name>
    <message>
      <source>action.apply</source>
      <translation>تطبيق</translation>
    </message>
    <message>
      <source>action.cancel</source>
      <translation>إلغاء</translation>
    </message>
    <message>
      <source>action.choose</source>
      <translation>اختيار</translation>
    </message>
    <message>
      <source>action.close</source>
      <translation>إغلاق</translation>
    </message>
    <message>
      <source>action.continue</source>
      <translation>متابعة</translation>
    </message>
    <message>
      <source>action.continue_next_period</source>
      <translation>استمر وابدأ الفترة التالية</translation>
    </message>
    <message>
      <source>action.open</source>
      <translation>فتح</translation>
    </message>
    <message>
      <source>action.open_main_window</source>
      <translation>فتح النافذة الرئيسية</translation>
    </message>
    <message>
      <source>action.pause</source>
      <translation>إيقاف مؤقت</translation>
    </message>
    <message>
      <source>action.preview</source>
      <translation>معاينة</translation>
    </message>
    <message>
      <source>action.refresh</source>
      <translation>تحديث</translation>
    </message>
    <message>
      <source>action.reset</source>
      <translation>إعادة ضبط</translation>
    </message>
    <message>
      <source>action.show</source>
      <translation>عرض</translation>
    </message>
    <message>
      <source>action.skip</source>
      <translation>تخطّي</translation>
    </message>
    <message>
      <source>action.start</source>
      <translation>ابدأ</translation>
    </message>
    <message>
      <source>dialog.color.choose</source>
      <translation>اختر لونًا</translation>
    </message>
    <message>
      <source>dialog.color.invalid_hex</source>
      <translation>قم بتصحيح القيم: مطلوب تنسيق #RRGBB.</translation>
    </message>
    <message>
      <source>dialog.color.title</source>
      <translation>لون</translation>
    </message>
    <message>
      <source>error.autostart.python_unavailable</source>
      <translation>التشغيل التلقائي متاح فقط في حزمة EXE. لا يمكن تمكينه عند التشغيل من Python.</translation>
    </message>
    <message>
      <source>error.data.portable_fallback</source>
      <translation>لا يمكن كتابة البيانات بجوار التطبيق. سيتم تخزين الإعدادات مؤقتًا في مجلد المستخدم الخاص بك. بالنسبة للوضع المحمول، انقل التطبيق إلى مجلد قابل للكتابة.</translation>
    </message>
    <message>
      <source>error.data.portable_title</source>
      <translation>الوضع المحمول</translation>
    </message>
    <message>
      <source>error.data.unavailable</source>
      <translation>لا يمكن إنشاء مجلد إعدادات التطبيق.</translation>
    </message>
    <message>
      <source>error.widget.hide</source>
      <translation>لا يمكن إخفاء القطعة: {error}</translation>
    </message>
    <message>
      <source>error.widget.show</source>
      <translation>لا يمكن إظهار القطعة: {error}</translation>
    </message>
    <message>
      <source>error.widget.state_mismatch</source>
      <translation>النافذة لم تدخل الحالة المطلوبة</translation>
    </message>
    <message>
      <source>help.content</source>
      <translation># بومودورو الموقت

## بداية سريعة

اختر الفترات في الإعدادات، وافتح المؤقت، وحدد **ابدأ**. استخدم المفتاح الموجود في الأعلى للتغيير بين الوضع الفاتح والداكن على الفور. تستخدم الإعدادات الثنائية المفاتيح؛ تبقى الإجراءات العادية الأزرار.

## الضوابط الموقت

- **البدء** تبدأ الفترة الحالية.
- **إيقاف مؤقت / متابعة** يتوقف مؤقتًا ويستأنف فترة منتظمة.
- **تخطي الفترة** ينتقل إلى الوضع التالي دون تسجيل المدة.
- **إعادة التعيين** تعود إلى العمل المتوقف وتسجل إعادة التعيين في الإحصائيات.
- يظهر **متابعة وبدء الفترة التالية** للانتقال اليدوي، ويسجل التجاوز مرة واحدة، ويبدأ الفترة التالية على الفور.

مع الانتقالات التلقائية، تبدأ الفترة التالية على الفور ولا يتم احتساب أي تجاوز. من خلال الانتقالات اليدوية، يعرض التطبيق **العمل الزائد**، **تجاوز فترات الراحة القصيرة**، أو **تجاوز فترات الراحة الطويلة**، والوقت مسبوقًا بـ `+`. يظل البدء والإيقاف المؤقت والتخطي وإعادة التعيين معطلاً أثناء التجاوز حتى لا يضيع أي وقت.

## المظهر وسهولة الوصول

تحتوي كل سمات Comet وAurora وWarm وCustom على أوضاع فاتحة ومظلمة. يقوم محرر السمات المخصصة بتخزين الأوضاع بشكل منفصل، والتحقق من صحة `#RRGGBB`، والتحذير عندما يكون التباين أقل من 4.5:1. إلغاء يستعيد الألوان المحفوظة؛ تؤدي إعادة الضبط إلى استعادة لوحة Comet الآمنة.

تتبع واجهة Qt Widgets مقياس Windows/Qt وتدعم تركيز لوحة المفاتيح. تعمل المفاتيح باستخدام الماوس أو "المسافة" أو "Enter"؛ يتم نقل حالتها من خلال الموضع واللون ونص التشغيل/الإيقاف. تستخدم أزرار الأوامر أيضًا "مسافة" أو "إدخال"، وتقدم تعليقات موجزة للصحافة، وتعرض مخططًا تفصيليًا عالي التباين فقط أثناء التنقل باستخدام لوحة المفاتيح. عند تعطيل الحركة، يحل تغيير اللون الفوري محل الرسوم المتحركة.

عند التشغيل لأول مرة، تستخدم النافذة الرئيسية حوالي 80% من الشاشة المتوفرة. يتذكر حجمه وموضعه ويعود إلى الشاشة المرئية بعد تغيير الدقة. عند العرض المتوسط ​​والضيق، يتم طي التنقل إلى أيقونات تحتوي على تلميحات أدوات، والتفاف مجموعات الأزرار، وتمرير الإعدادات دون قص الإجراءات المثبتة.

يقوم الوضع الداكن بتصميم إطار العرض وقائمة الدرج ويطلب شريط عنوان أصلي داكن عندما يدعمه Windows DWM. يتم استخدام رمز الطماطم والمؤقت الأصلي للنوافذ وشريط المهام والدرج وملف EXE المعبأ.

## إشارة التجاوز

اختر النبض، أو الأرقام المكبرة، أو إشارات الإشارة، أو حدود التمييز، أو مؤشر الموجة، أو عدم وجود رسوم متحركة. يتم تكوين تغييرات اللون والنطاق والسرعة والكثافة وثلاثة ألوان بشكل مستقل. لا تؤدي المعاينة إلى تعديل المؤقت أو الإحصائيات أو الإشعارات أو العتامة.

تتلقى النافذة الرئيسية والقطعة نفس إطار التأثير. يؤدي الاستمرار أو الخروج إلى استعادة الألوان والأحجام العادية على الفور. مع تعطيل الحركة، يظل مؤشر الوصول الثابت واسم الحالة والعلامة `+`.

## القطعة العائمة

يقوم مفتاح **إظهار القطعة** الموجود في صفحة المؤقت بعرض وإخفاء نفس النافذة. تتوفر سبعة تخطيطات: Minimal، Compact، Expanded، Micro، Row، Ring، وScoreboard. جميعهم يستخدمون نفس "TimerEngine".

يتم تخزين النوع والحجم والموضع بشكل منفصل لكل تخطيط. يؤدي تغيير الحجم يدويًا إلى إنشاء حجم مخصص. تتراوح نسبة التعتيم من 5 إلى 100%؛ أثناء التجاوز، يمكن أن تصبح الأداة معتمة تمامًا مؤقتًا ثم تعود إلى القيمة المحفوظة بالضبط.

في العرض الموسع، يقوم شريط الإجراءات الضيق بتغليف الإجراءات بأكملها. لا يتم اختصار "المتابعة" أبدًا. عند الحد الأدنى للعرض فقط، قد يصبح "فتح" رمزًا بتلميح أداة؛ تلتف الإجراءات المتبقية إلى الصف التالي.

## الإخطارات والإحصاءات والصينية

يمكن إغلاق إشعار النقل التلقائي. يتضمن الإخطار اليدوي متابعة؛ يقوم زر الإغلاق الخاص به بإغلاق النافذة فقط ولا يفقد وقت التجاوز. يظل نفس الأمر متاحًا في النافذة الرئيسية والقطعة.

تفصل الإحصائيات بين العمل المنتظم وفترات الراحة المنتظمة وثلاثة أنواع من التجاوزات لهذا اليوم وفي كل الأوقات. يمكن أن يؤدي إغلاق النافذة الرئيسية إلى تقليل حجم التطبيق إلى الدرج. يؤدي الخروج الكامل العادي إلى توفير وقت التجاوز المتراكم.

يتم تشغيل مثيل تطبيق واحد لكل مستخدم Windows. يُظهر التشغيل الثاني رسالة النظام دون إنشاء واجهة أخرى.</translation>
    </message>
    <message>
      <source>help.subtitle</source>
      <translation>الميزات وسلوك التطبيق الآمن.</translation>
    </message>
    <message>
      <source>help.title</source>
      <translation>يساعد</translation>
    </message>
    <message>
      <source>main.brand_subtitle</source>
      <translation>إيقاع عمل هادئ</translation>
    </message>
    <message>
      <source>nav.help</source>
      <translation>يساعد</translation>
    </message>
    <message>
      <source>nav.settings</source>
      <translation>إعدادات</translation>
    </message>
    <message>
      <source>nav.statistics</source>
      <translation>إحصائيات</translation>
    </message>
    <message>
      <source>nav.timer</source>
      <translation>الموقت</translation>
    </message>
    <message>
      <source>notification.auto_transition</source>
      <translation>{completed}

لقد بدأت الفترة التالية بالفعل: {next_period}.</translation>
    </message>
    <message>
      <source>notification.completed.long_break</source>
      <translation>اكتملت الاستراحة الطويلة.</translation>
    </message>
    <message>
      <source>notification.completed.short_break</source>
      <translation>اكتملت الاستراحة القصيرة.</translation>
    </message>
    <message>
      <source>notification.completed.work</source>
      <translation>انتهت فترة العمل.</translation>
    </message>
    <message>
      <source>notification.default.long_break_end</source>
      <translation>اكتملت الاستراحة الطويلة. حان الوقت لبدء فترة عمل جديدة.</translation>
    </message>
    <message>
      <source>notification.default.short_break_end</source>
      <translation>اكتملت الاستراحة القصيرة. حان الوقت للعودة إلى العمل.</translation>
    </message>
    <message>
      <source>notification.default.work_end</source>
      <translation>انتهت فترة العمل. حان الوقت للاستراحة.</translation>
    </message>
    <message>
      <source>notification.manual_transition</source>
      <translation>{completed}

حدد متابعة لبدء {next_period}.</translation>
    </message>
    <message>
      <source>overrun.effect.beacons</source>
      <translation>منارات الإشارة</translation>
    </message>
    <message>
      <source>overrun.effect.border</source>
      <translation>إطار مميز</translation>
    </message>
    <message>
      <source>overrun.effect.none</source>
      <translation>بدون حركة</translation>
    </message>
    <message>
      <source>overrun.effect.pulse</source>
      <translation>نبض</translation>
    </message>
    <message>
      <source>overrun.effect.scale</source>
      <translation>تكبير الأرقام</translation>
    </message>
    <message>
      <source>overrun.effect.wave</source>
      <translation>مؤشر الموجة</translation>
    </message>
    <message>
      <source>overrun.intensity.medium</source>
      <translation>متوسط</translation>
    </message>
    <message>
      <source>overrun.intensity.strong</source>
      <translation>قوي</translation>
    </message>
    <message>
      <source>overrun.intensity.weak</source>
      <translation>خفيف</translation>
    </message>
    <message>
      <source>overrun.scope.both</source>
      <translation>الأرقام وبطاقة الموقت</translation>
    </message>
    <message>
      <source>overrun.scope.card</source>
      <translation>بطاقة الموقت</translation>
    </message>
    <message>
      <source>overrun.scope.digits</source>
      <translation>أرقام الموقت فقط</translation>
    </message>
    <message>
      <source>overrun.speed.fast</source>
      <translation>سريع</translation>
    </message>
    <message>
      <source>overrun.speed.normal</source>
      <translation>طبيعي</translation>
    </message>
    <message>
      <source>overrun.speed.slow</source>
      <translation>بطيء</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode</source>
      <translation>الوضع المظلم</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode.description</source>
      <translation>إيقاف - الوضع الفاتح، تشغيل - الوضع المظلم.</translation>
    </message>
    <message>
      <source>settings.appearance.edit_colors</source>
      <translation>تخصيص الألوان</translation>
    </message>
    <message>
      <source>settings.appearance.editor_unavailable</source>
      <translation>المحرر غير متوفر في هذه النافذة.</translation>
    </message>
    <message>
      <source>settings.appearance.language</source>
      <translation>لغة الواجهة</translation>
    </message>
    <message>
      <source>settings.appearance.subtitle</source>
      <translation>تقوم اللوحات الكاملة بتحديث كل نافذة مفتوحة دون إعادة تشغيل.</translation>
    </message>
    <message>
      <source>settings.appearance.title</source>
      <translation>مظهر</translation>
    </message>
    <message>
      <source>settings.logic.long_break_interval</source>
      <translation>فترات العمل قبل فترة راحة طويلة</translation>
    </message>
    <message>
      <source>settings.logic.subtitle</source>
      <translation>ترتيب العمل، فترات الراحة القصيرة، فترات الراحة الطويلة.</translation>
    </message>
    <message>
      <source>settings.logic.title</source>
      <translation>سلوك الموقت</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break</source>
      <translation>استخدم فترات راحة طويلة</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break.description</source>
      <translation>بعد مرور عدد محدد من فترات العمل.</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition</source>
      <translation>الانتقال التلقائي</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition.description</source>
      <translation>تشغيل - تبدأ الفترة التالية على الفور؛ OFF — يتم حساب وقت التجاوز.</translation>
    </message>
    <message>
      <source>settings.notifications.enabled</source>
      <translation>إشعارات</translation>
    </message>
    <message>
      <source>settings.notifications.long_break_end</source>
      <translation>استكمال استراحة طويلة</translation>
    </message>
    <message>
      <source>settings.notifications.short_break_end</source>
      <translation>الانتهاء من استراحة قصيرة</translation>
    </message>
    <message>
      <source>settings.notifications.sound</source>
      <translation>صوت الإخطار</translation>
    </message>
    <message>
      <source>settings.notifications.subtitle</source>
      <translation>يمكن دائمًا إكمال النقل اليدوي من النافذة الرئيسية أو الأداة.</translation>
    </message>
    <message>
      <source>settings.notifications.title</source>
      <translation>إشعارات</translation>
    </message>
    <message>
      <source>settings.notifications.work_end</source>
      <translation>الانتهاء من العمل</translation>
    </message>
    <message>
      <source>settings.overrun.allow_motion</source>
      <translation>السماح بحركة التأثير</translation>
    </message>
    <message>
      <source>settings.overrun.change_color</source>
      <translation>تغيير لون الموقت</translation>
    </message>
    <message>
      <source>settings.overrun.color_dialog</source>
      <translation>تجاوز اللون</translation>
    </message>
    <message>
      <source>settings.overrun.effect</source>
      <translation>التأثير الأساسي</translation>
    </message>
    <message>
      <source>settings.overrun.intensity</source>
      <translation>شدة</translation>
    </message>
    <message>
      <source>settings.overrun.invalid_colors</source>
      <translation>تم استبدال الألوان غير الصالحة بقيم من السمة النشطة.</translation>
    </message>
    <message>
      <source>settings.overrun.opaque_widget</source>
      <translation>اجعل القطعة غير شفافة أثناء التجاوز</translation>
    </message>
    <message>
      <source>settings.overrun.scope</source>
      <translation>منطقة تغيير اللون</translation>
    </message>
    <message>
      <source>settings.overrun.separate_colors</source>
      <translation>ألوان منفصلة</translation>
    </message>
    <message>
      <source>settings.overrun.speed</source>
      <translation>سرعة</translation>
    </message>
    <message>
      <source>settings.overrun.subtitle</source>
      <translation>يتم تطبيق إطار مشترك واحد على النافذة الرئيسية والقطعة المفتوحة.</translation>
    </message>
    <message>
      <source>settings.overrun.title</source>
      <translation>إشارة التجاوز</translation>
    </message>
    <message>
      <source>settings.overrun.use_theme_color</source>
      <translation>استخدام لون الموضوع</translation>
    </message>
    <message>
      <source>settings.profiles.apply</source>
      <translation>تطبيق الملف الشخصي</translation>
    </message>
    <message>
      <source>settings.profiles.default_cannot_delete</source>
      <translation>لا يمكن حذف ملف التعريف الافتراضي.</translation>
    </message>
    <message>
      <source>settings.profiles.default_name</source>
      <translation>تقصير</translation>
    </message>
    <message>
      <source>settings.profiles.defaults</source>
      <translation>الإعدادات الافتراضية</translation>
    </message>
    <message>
      <source>settings.profiles.delete</source>
      <translation>حذف الملف الشخصي</translation>
    </message>
    <message>
      <source>settings.profiles.delete_confirmation</source>
      <translation>هل تريد حذف الملف الشخصي "{profile_name}"؟</translation>
    </message>
    <message>
      <source>settings.profiles.delete_title</source>
      <translation>حذف الملف الشخصي</translation>
    </message>
    <message>
      <source>settings.profiles.dialog_title</source>
      <translation>حساب تعريفي</translation>
    </message>
    <message>
      <source>settings.profiles.enter_name</source>
      <translation>أدخل اسم الملف الشخصي.</translation>
    </message>
    <message>
      <source>settings.profiles.name_placeholder</source>
      <translation>اسم الملف الشخصي</translation>
    </message>
    <message>
      <source>settings.profiles.restore_personal</source>
      <translation>استعادة الإعدادات الخاصة بي</translation>
    </message>
    <message>
      <source>settings.profiles.save</source>
      <translation>حفظ الملف الشخصي</translation>
    </message>
    <message>
      <source>settings.profiles.select_profile</source>
      <translation>حدد ملف تعريف من القائمة.</translation>
    </message>
    <message>
      <source>settings.profiles.subtitle</source>
      <translation>احفظ مجموعات من المدد وخيارات المظهر وإعدادات عناصر واجهة المستخدم.</translation>
    </message>
    <message>
      <source>settings.profiles.title</source>
      <translation>الملفات الشخصية</translation>
    </message>
    <message>
      <source>settings.save</source>
      <translation>حفظ الإعدادات</translation>
    </message>
    <message>
      <source>settings.section.appearance</source>
      <translation>مظهر</translation>
    </message>
    <message>
      <source>settings.section.logic</source>
      <translation>سلوك الموقت</translation>
    </message>
    <message>
      <source>settings.section.notifications</source>
      <translation>إشعارات</translation>
    </message>
    <message>
      <source>settings.section.overrun</source>
      <translation>تجاوز</translation>
    </message>
    <message>
      <source>settings.section.profiles</source>
      <translation>الملفات الشخصية</translation>
    </message>
    <message>
      <source>settings.section.time</source>
      <translation>وقت</translation>
    </message>
    <message>
      <source>settings.section.tray</source>
      <translation>علبة وبدء التشغيل التلقائي</translation>
    </message>
    <message>
      <source>settings.section.widget</source>
      <translation>القطعة</translation>
    </message>
    <message>
      <source>settings.subtitle</source>
      <translation>يتم تطبيق تغييرات السمة والقطعة على الفور؛ تنطبق التغييرات الأخرى بعد الحفظ.</translation>
    </message>
    <message>
      <source>settings.time.format</source>
      <translation>تنسيق الوقت</translation>
    </message>
    <message>
      <source>settings.time.long_break_minutes</source>
      <translation>استراحة طويلة، دقائق</translation>
    </message>
    <message>
      <source>settings.time.short_break_minutes</source>
      <translation>استراحة قصيرة، دقائق</translation>
    </message>
    <message>
      <source>settings.time.subtitle</source>
      <translation>يتم تطبيق المدد بأمان عند الحفظ.</translation>
    </message>
    <message>
      <source>settings.time.title</source>
      <translation>وقت</translation>
    </message>
    <message>
      <source>settings.time.work_minutes</source>
      <translation>العمل، دقائق</translation>
    </message>
    <message>
      <source>settings.title</source>
      <translation>إعدادات</translation>
    </message>
    <message>
      <source>settings.tray.autostart</source>
      <translation>ابدأ مع ويندوز</translation>
    </message>
    <message>
      <source>settings.tray.autostart_current</source>
      <translation>يتم تمكين التشغيل التلقائي ويشير إلى المجلد الحالي للتطبيق.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_disabled</source>
      <translation>تم تعطيل التشغيل التلقائي.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_python</source>
      <translation>التشغيل من Python: يمكن تمكين التشغيل التلقائي في إصدار EXE.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_stale</source>
      <translation>مسار التشغيل التلقائي قديم. قم بتحديثه بعد نقل التطبيق.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_title</source>
      <translation>تشغيل تلقائي</translation>
    </message>
    <message>
      <source>settings.tray.close_to_tray</source>
      <translation>تصغير إلى الدرج عند الإغلاق</translation>
    </message>
    <message>
      <source>settings.tray.minimize_on_start</source>
      <translation>تصغير التطبيق بعد الإطلاق</translation>
    </message>
    <message>
      <source>settings.tray.subtitle</source>
      <translation>تعمل علبة النظام في مؤشر ترابط Qt GUI المشترك.</translation>
    </message>
    <message>
      <source>settings.tray.title</source>
      <translation>علبة وبدء التشغيل التلقائي</translation>
    </message>
    <message>
      <source>settings.tray.update_autostart</source>
      <translation>تحديث مسار التشغيل التلقائي</translation>
    </message>
    <message>
      <source>settings.widget.always_on_top</source>
      <translation>دائمًا في المقدمة</translation>
    </message>
    <message>
      <source>settings.widget.dialog_title</source>
      <translation>القطعة</translation>
    </message>
    <message>
      <source>settings.widget.opacity</source>
      <translation>عتامة القطعة</translation>
    </message>
    <message>
      <source>settings.widget.opacity.description</source>
      <translation>القيم المنخفضة تجعل الأداة أكثر شفافية. الحد الأدنى — 5%.</translation>
    </message>
    <message>
      <source>settings.widget.position_reset</source>
      <translation>تمت إعادة تعيين موضع النوع الحالي.</translation>
    </message>
    <message>
      <source>settings.widget.reset_position</source>
      <translation>إعادة تعيين الموقف للنوع الحالي</translation>
    </message>
    <message>
      <source>settings.widget.size</source>
      <translation>مقاس</translation>
    </message>
    <message>
      <source>settings.widget.subtitle</source>
      <translation>يتم التحكم في الرؤية عن طريق المفتاح الموجود على صفحة المؤقت.</translation>
    </message>
    <message>
      <source>settings.widget.title</source>
      <translation>القطعة العائمة</translation>
    </message>
    <message>
      <source>settings.widget.type</source>
      <translation>نوع القطعة</translation>
    </message>
    <message>
      <source>startup.already_running</source>
      <translation>يبدأ مؤقت بومودورو أو أنه قيد التشغيل بالفعل. انتظر حتى تفتح النافذة أو استخدم التطبيق المفتوح بالفعل.</translation>
    </message>
    <message>
      <source>startup.lock.already_running</source>
      <translation>هناك مثيل تطبيق آخر قيد التشغيل بالفعل.</translation>
    </message>
    <message>
      <source>startup.lock.create_failed</source>
      <translation>تعذر إنشاء قفل النظام (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.release_failed</source>
      <translation>تعذر تحرير قفل النظام (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.secondary_close_failed</source>
      <translation>هناك مثيل آخر قيد التشغيل بالفعل، ولكن لا يمكن إغلاق المقبض الثانوي الخاص به (WinError {error_code}).</translation>
    </message>
    <message>
      <source>startup.lock.unsupported</source>
      <translation>يتم دعم قفل النظام ذو المثيل الفردي فقط على نظام التشغيل Windows.</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_cycles</source>
      <translation>
        <numerusform>دورات كاملة</numerusform>
        <numerusform>دورة كاملة</numerusform>
        <numerusform>دورتان كاملتان</numerusform>
        <numerusform>دورات كاملة</numerusform>
        <numerusform>دورة كاملة</numerusform>
        <numerusform>دورة كاملة</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_long_breaks</source>
      <translation>
        <numerusform>فترات راحة طويلة</numerusform>
        <numerusform>استراحة طويلة</numerusform>
        <numerusform>استراحتان طويلتان</numerusform>
        <numerusform>فترات راحة طويلة</numerusform>
        <numerusform>استراحة طويلة</numerusform>
        <numerusform>استراحة طويلة</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_short_breaks</source>
      <translation>
        <numerusform>فترات راحة قصيرة</numerusform>
        <numerusform>استراحة قصيرة</numerusform>
        <numerusform>استراحتان قصيرتان</numerusform>
        <numerusform>فترات راحة قصيرة</numerusform>
        <numerusform>استراحة قصيرة</numerusform>
        <numerusform>استراحة قصيرة</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_work_periods</source>
      <translation>
        <numerusform>فترات عمل</numerusform>
        <numerusform>فترة عمل</numerusform>
        <numerusform>فترتا عمل</numerusform>
        <numerusform>فترات عمل</numerusform>
        <numerusform>فترة عمل</numerusform>
        <numerusform>فترة عمل</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.long_break_overrun</source>
      <translation>تجاوز فترة الاستراحة الطويلة</translation>
    </message>
    <message>
      <source>stats.metric.overwork_time</source>
      <translation>وقت العمل الزائد</translation>
    </message>
    <message>
      <source>stats.metric.rest_time</source>
      <translation>وقت الاستراحة</translation>
    </message>
    <message>
      <source>stats.metric.short_break_overrun</source>
      <translation>تجاوز فترة الاستراحة القصيرة</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.skipped_periods</source>
      <translation>
        <numerusform>فترات متخطاة</numerusform>
        <numerusform>فترة متخطاة</numerusform>
        <numerusform>فترتان متخطاتان</numerusform>
        <numerusform>فترات متخطاة</numerusform>
        <numerusform>فترة متخطاة</numerusform>
        <numerusform>فترة متخطاة</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.timer_resets</source>
      <translation>
        <numerusform>مرات إعادة ضبط</numerusform>
        <numerusform>إعادة ضبط واحدة</numerusform>
        <numerusform>مرتا إعادة ضبط</numerusform>
        <numerusform>مرات إعادة ضبط</numerusform>
        <numerusform>مرة إعادة ضبط</numerusform>
        <numerusform>إعادة ضبط</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.work_time</source>
      <translation>وقت العمل</translation>
    </message>
    <message>
      <source>stats.period.all_time</source>
      <translation>كل الوقت</translation>
    </message>
    <message>
      <source>stats.period.today</source>
      <translation>اليوم</translation>
    </message>
    <message>
      <source>stats.reset.action</source>
      <translation>إعادة تعيين الإحصائيات</translation>
    </message>
    <message>
      <source>stats.reset.confirmation</source>
      <translation>هل أنت متأكد أنك تريد حذف جميع الإحصائيات؟</translation>
    </message>
    <message>
      <source>stats.reset.title</source>
      <translation>إعادة تعيين الإحصائيات</translation>
    </message>
    <message>
      <source>stats.subtitle</source>
      <translation>يتم تعقب الوقت العادي والتجاوزات بشكل منفصل.</translation>
    </message>
    <message>
      <source>stats.title</source>
      <translation>إحصائيات</translation>
    </message>
    <message>
      <source>theme.appearance.dark</source>
      <translation>داكن</translation>
    </message>
    <message>
      <source>theme.appearance.light</source>
      <translation>فاتح</translation>
    </message>
    <message>
      <source>theme.contrast.accent</source>
      <translation>لهجة النص / لهجة</translation>
    </message>
    <message>
      <source>theme.contrast.button</source>
      <translation>نص الزر / الزر</translation>
    </message>
    <message>
      <source>theme.contrast.long_break</source>
      <translation>استراحة طويلة / بطاقة</translation>
    </message>
    <message>
      <source>theme.contrast.long_break_overrun</source>
      <translation>تجاوز الاستراحة الطويلة / البطاقة</translation>
    </message>
    <message>
      <source>theme.contrast.overwork</source>
      <translation>إرهاق / بطاقة</translation>
    </message>
    <message>
      <source>theme.contrast.primary_card</source>
      <translation>النص الأساسي / البطاقة</translation>
    </message>
    <message>
      <source>theme.contrast.secondary_card</source>
      <translation>النص الثانوي / البطاقة</translation>
    </message>
    <message>
      <source>theme.contrast.short_break</source>
      <translation>استراحة قصيرة / بطاقة</translation>
    </message>
    <message>
      <source>theme.contrast.short_break_overrun</source>
      <translation>تجاوز / بطاقة استراحة قصيرة</translation>
    </message>
    <message>
      <source>theme.contrast.work</source>
      <translation>العمل / البطاقة</translation>
    </message>
    <message>
      <source>theme.description.aurora</source>
      <translation>لهجات باردة باللون الأزرق والبنفسجي</translation>
    </message>
    <message>
      <source>theme.description.comet</source>
      <translation>لوحة محايدة هادئة</translation>
    </message>
    <message>
      <source>theme.description.custom</source>
      <translation>لوحاتك الفاتحة والداكنة المستقلة</translation>
    </message>
    <message>
      <source>theme.description.warm</source>
      <translation>الأسطح الرملية الناعمة والدافئة</translation>
    </message>
    <message>
      <source>theme.name.aurora</source>
      <translation>أورورا</translation>
    </message>
    <message>
      <source>theme.name.comet</source>
      <translation>المذنب</translation>
    </message>
    <message>
      <source>theme.name.custom</source>
      <translation>مخصص</translation>
    </message>
    <message>
      <source>theme.name.warm</source>
      <translation>دافيء</translation>
    </message>
    <message>
      <source>theme_editor.color.accent</source>
      <translation>لهجة</translation>
    </message>
    <message>
      <source>theme_editor.color.accent_hover</source>
      <translation>تحوم</translation>
    </message>
    <message>
      <source>theme_editor.color.background</source>
      <translation>الخلفية الرئيسية</translation>
    </message>
    <message>
      <source>theme_editor.color.border</source>
      <translation>الحدود</translation>
    </message>
    <message>
      <source>theme_editor.color.button_background</source>
      <translation>لون الزر</translation>
    </message>
    <message>
      <source>theme_editor.color.button_text</source>
      <translation>نص الزر</translation>
    </message>
    <message>
      <source>theme_editor.color.card_background</source>
      <translation>خلفية البطاقة</translation>
    </message>
    <message>
      <source>theme_editor.color.disabled</source>
      <translation>العناصر المعطلة</translation>
    </message>
    <message>
      <source>theme_editor.color.error</source>
      <translation>خطأ</translation>
    </message>
    <message>
      <source>theme_editor.color.focus</source>
      <translation>ركز</translation>
    </message>
    <message>
      <source>theme_editor.color.on_accent</source>
      <translation>نص زر التمييز</translation>
    </message>
    <message>
      <source>theme_editor.color.secondary_background</source>
      <translation>الخلفية الثانوية</translation>
    </message>
    <message>
      <source>theme_editor.color.success</source>
      <translation>نجاح</translation>
    </message>
    <message>
      <source>theme_editor.color.text_primary</source>
      <translation>النص الأساسي</translation>
    </message>
    <message>
      <source>theme_editor.color.text_secondary</source>
      <translation>النص الثانوي</translation>
    </message>
    <message>
      <source>theme_editor.color.warning</source>
      <translation>تحذير</translation>
    </message>
    <message>
      <source>theme_editor.contrast.ok</source>
      <translation>التحقق من التباين: تتوافق المجموعات الرئيسية مع المبادئ التوجيهية 4.5:1.</translation>
    </message>
    <message numerus="yes">
      <source>theme_editor.contrast.warning</source>
      <translation>
        <numerusform>فحص التباين: {count} مجموعة أقل من 4.5:1.</numerusform>
        <numerusform>فحص التباين: {count} مجموعة أقل من 4.5:1. يلزم التأكيد عند التطبيق.</numerusform>
        <numerusform>فحص التباين: {count} مجموعتان أقل من 4.5:1. يلزم التأكيد عند التطبيق.</numerusform>
        <numerusform>فحص التباين: {count} مجموعات أقل من 4.5:1. يلزم التأكيد عند التطبيق.</numerusform>
        <numerusform>فحص التباين: {count} مجموعة أقل من 4.5:1. يلزم التأكيد عند التطبيق.</numerusform>
        <numerusform>فحص التباين: {count} مجموعة أقل من 4.5:1. يلزم التأكيد عند التطبيق.</numerusform>
      </translation>
    </message>
    <message>
      <source>theme_editor.create_copy</source>
      <translation>إنشاء نسخة</translation>
    </message>
    <message>
      <source>theme_editor.create_from</source>
      <translation>إنشاء من</translation>
    </message>
    <message>
      <source>theme_editor.editing_mode</source>
      <translation>جارٍ تحرير الوضع</translation>
    </message>
    <message>
      <source>theme_editor.group.service_states</source>
      <translation>ألوان الحالة</translation>
    </message>
    <message>
      <source>theme_editor.group.surfaces</source>
      <translation>الأسطح</translation>
    </message>
    <message>
      <source>theme_editor.group.text_controls</source>
      <translation>النص والضوابط</translation>
    </message>
    <message>
      <source>theme_editor.group.timer_states</source>
      <translation>حالات الموقت</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.confirmation</source>
      <translation>بعض المجموعات أقل من 4.5:1:

{details}

هل تريد الحفظ على أي حال؟</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.title</source>
      <translation>تباين منخفض</translation>
    </message>
    <message>
      <source>theme_editor.reset.confirmation</source>
      <translation>هل تريد إعادة ضبط كلا الوضعين على سمة المذنب الآمنة؟</translation>
    </message>
    <message>
      <source>theme_editor.reset.title</source>
      <translation>إعادة تعيين الموضوع</translation>
    </message>
    <message>
      <source>theme_editor.reset_all</source>
      <translation>إعادة تعيين الموضوع بأكمله</translation>
    </message>
    <message>
      <source>theme_editor.reset_mode</source>
      <translation>إعادة ضبط الوضع الحالي</translation>
    </message>
    <message>
      <source>theme_editor.subtitle</source>
      <translation>تحرير الأوضاع الفاتحة والداكنة بشكل مستقل.</translation>
    </message>
    <message>
      <source>theme_editor.title</source>
      <translation>موضوع مخصص</translation>
    </message>
    <message>
      <source>timer.mode.long_break</source>
      <translation>استراحة طويلة</translation>
    </message>
    <message>
      <source>timer.mode.long_break_overrun</source>
      <translation>تجاوز مدة الاستراحة الطويلة</translation>
    </message>
    <message>
      <source>timer.mode.overwork</source>
      <translation>استمرار العمل</translation>
    </message>
    <message>
      <source>timer.mode.short_break</source>
      <translation>استراحة قصيرة</translation>
    </message>
    <message>
      <source>timer.mode.short_break_overrun</source>
      <translation>تجاوز مدة الاستراحة القصيرة</translation>
    </message>
    <message>
      <source>timer.mode.work</source>
      <translation>عمل</translation>
    </message>
    <message>
      <source>timer.overrun.waiting_status</source>
      <translation>اكتملت الفترة — يتم احتساب التجاوز حتى المتابعة</translation>
    </message>
    <message>
      <source>timer.page.subtitle</source>
      <translation>مؤقت واحد للنافذة الرئيسية والإشعارات والقطعة.</translation>
    </message>
    <message>
      <source>timer.page.title</source>
      <translation>جلسة التركيز</translation>
    </message>
    <message>
      <source>timer.status.accessible_name</source>
      <translation>حالة الموقت</translation>
    </message>
    <message>
      <source>timer.status.overrun</source>
      <translation>يتم احتساب الوقت الزائد</translation>
    </message>
    <message>
      <source>timer.status.paused</source>
      <translation>توقف الموقّت مؤقتًا</translation>
    </message>
    <message>
      <source>timer.status.running</source>
      <translation>تشغيل الموقت</translation>
    </message>
    <message>
      <source>timer.status.stopped</source>
      <translation>توقف الموقت</translation>
    </message>
    <message>
      <source>timer.widget.show</source>
      <translation>إظهار القطعة</translation>
    </message>
    <message>
      <source>timer.widget.show.description</source>
      <translation>يتم حفظ الموضع والحجم والنوع والعتامة بشكل منفصل.</translation>
    </message>
    <message>
      <source>toggle.accessible_description</source>
      <translation>تشغيل - ممكّن، إيقاف - معطل</translation>
    </message>
    <message>
      <source>toggle.accessible_name</source>
      <translation>يُحوّل</translation>
    </message>
    <message>
      <source>toggle.off</source>
      <translation>عن</translation>
    </message>
    <message>
      <source>toggle.on</source>
      <translation>على</translation>
    </message>
    <message>
      <source>toggle.state.off</source>
      <translation>إيقاف، معطل</translation>
    </message>
    <message>
      <source>toggle.state.on</source>
      <translation>تشغيل، تمكين</translation>
    </message>
    <message>
      <source>tray.exit</source>
      <translation>إنهاء</translation>
    </message>
    <message>
      <source>tray.hide</source>
      <translation>إخفاء النافذة</translation>
    </message>
    <message>
      <source>tray.reset</source>
      <translation>إعادة ضبط</translation>
    </message>
    <message>
      <source>tray.show</source>
      <translation>عرض النافذة</translation>
    </message>
    <message>
      <source>tray.start_pause</source>
      <translation>بدء / إيقاف مؤقت</translation>
    </message>
    <message numerus="yes">
      <source>widget.completed_work_periods</source>
      <translation>
        <numerusform>فترات العمل المكتملة: {count}</numerusform>
        <numerusform>فترة العمل المكتملة: {count}</numerusform>
        <numerusform>فترتا العمل المكتملتان: {count}</numerusform>
        <numerusform>فترات العمل المكتملة: {count}</numerusform>
        <numerusform>فترة العمل المكتملة: {count}</numerusform>
        <numerusform>فترة العمل المكتملة: {count}</numerusform>
      </translation>
    </message>
    <message>
      <source>widget.size.custom</source>
      <translation>مخصص</translation>
    </message>
    <message>
      <source>widget.size.large</source>
      <translation>كبير</translation>
    </message>
    <message>
      <source>widget.size.medium</source>
      <translation>متوسط</translation>
    </message>
    <message>
      <source>widget.size.small</source>
      <translation>صغير</translation>
    </message>
    <message>
      <source>widget.type.compact</source>
      <translation>مدمج</translation>
    </message>
    <message>
      <source>widget.type.compact.description</source>
      <translation>بطاقة مدمجة كلاسيكية مع الإجراء الأساسي.</translation>
    </message>
    <message>
      <source>widget.type.expanded</source>
      <translation>موسّع</translation>
    </message>
    <message>
      <source>widget.type.expanded.description</source>
      <translation>معلومات الدورة والمجموعة الكاملة من إجراءات المؤقت الأساسي.</translation>
    </message>
    <message>
      <source>widget.type.micro</source>
      <translation>مايكرو</translation>
    </message>
    <message>
      <source>widget.type.micro.description</source>
      <translation>أصغر نافذة: عادة الوقت فقط.</translation>
    </message>
    <message>
      <source>widget.type.minimal</source>
      <translation>بسيط</translation>
    </message>
    <message>
      <source>widget.type.minimal.description</source>
      <translation>وقت كبير، اسم الدولة، والحد الأدنى من التفاصيل.</translation>
    </message>
    <message>
      <source>widget.type.ring</source>
      <translation>حلقة</translation>
    </message>
    <message>
      <source>widget.type.ring.description</source>
      <translation>الوقت داخل مؤشر الفترة الدائرية.</translation>
    </message>
    <message>
      <source>widget.type.row</source>
      <translation>صف</translation>
    </message>
    <message>
      <source>widget.type.row.description</source>
      <translation>صف أفقي لحافة الشاشة.</translation>
    </message>
    <message>
      <source>widget.type.scoreboard</source>
      <translation>لوحة النتائج</translation>
    </message>
    <message>
      <source>widget.type.scoreboard.description</source>
      <translation>أرقام كبيرة أحادية المسافة بأسلوب لوحة النتائج الهادئة.</translation>
    </message>
    <message>
      <source>widget.window_title</source>
      <translation>القطعة بومودورو</translation>
    </message>
  </context>
  <context>
    <name>QPlatformTheme</name>
    <message>
      <source>OK</source>
      <translation>موافق</translation>
    </message>
    <message>
      <source>Save</source>
      <translation>حفظ</translation>
    </message>
    <message>
      <source>Save All</source>
      <translation>حفظ الكل</translation>
    </message>
    <message>
      <source>Open</source>
      <translation>فتح</translation>
    </message>
    <message>
      <source>&amp;Yes</source>
      <translation>&amp;نعم</translation>
    </message>
    <message>
      <source>Yes to &amp;All</source>
      <translation>نعم لل&amp;كل</translation>
    </message>
    <message>
      <source>&amp;No</source>
      <translation>&amp;لا</translation>
    </message>
    <message>
      <source>N&amp;o to All</source>
      <translation>لا لل&amp;كل</translation>
    </message>
    <message>
      <source>Abort</source>
      <translation>إيقاف</translation>
    </message>
    <message>
      <source>Retry</source>
      <translation>إعادة المحاولة</translation>
    </message>
    <message>
      <source>Ignore</source>
      <translation>تجاهل</translation>
    </message>
    <message>
      <source>Close</source>
      <translation>إغلاق</translation>
    </message>
    <message>
      <source>Cancel</source>
      <translation>إلغاء</translation>
    </message>
    <message>
      <source>Discard</source>
      <translation>تجاهل التغييرات</translation>
    </message>
    <message>
      <source>Help</source>
      <translation>مساعدة</translation>
    </message>
    <message>
      <source>Apply</source>
      <translation>تطبيق</translation>
    </message>
    <message>
      <source>Reset</source>
      <translation>إعادة تعيين</translation>
    </message>
    <message>
      <source>Restore Defaults</source>
      <translation>استعادة الإعدادات الافتراضية</translation>
    </message>
  </context>
</TS>
