<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="hi_IN">
  <context>
    <name>PomodoroTimer</name>
    <message>
      <source>action.apply</source>
      <translation>लागू करें</translation>
    </message>
    <message>
      <source>action.cancel</source>
      <translation>रद्द करें</translation>
    </message>
    <message>
      <source>action.choose</source>
      <translation>चुनें</translation>
    </message>
    <message>
      <source>action.close</source>
      <translation>बंद करें</translation>
    </message>
    <message>
      <source>action.continue</source>
      <translation>जारी रखें</translation>
    </message>
    <message>
      <source>action.continue_next_period</source>
      <translation>जारी रखें और अगली अवधि शुरू करें</translation>
    </message>
    <message>
      <source>action.open</source>
      <translation>खोलें</translation>
    </message>
    <message>
      <source>action.open_main_window</source>
      <translation>मुख्य विंडो खोलें</translation>
    </message>
    <message>
      <source>action.pause</source>
      <translation>विराम</translation>
    </message>
    <message>
      <source>action.preview</source>
      <translation>पूर्वावलोकन</translation>
    </message>
    <message>
      <source>action.refresh</source>
      <translation>ताज़ा करें</translation>
    </message>
    <message>
      <source>action.reset</source>
      <translation>पुनः आरंभ करें</translation>
    </message>
    <message>
      <source>action.show</source>
      <translation>दिखाएँ</translation>
    </message>
    <message>
      <source>action.skip</source>
      <translation>छोड़ें</translation>
    </message>
    <message>
      <source>action.start</source>
      <translation>शुरू करें</translation>
    </message>
    <message>
      <source>dialog.color.choose</source>
      <translation>कोई रंग चुनें</translation>
    </message>
    <message>
      <source>dialog.color.invalid_hex</source>
      <translation>मान ठीक करें: #RRGGBB प्रारूप आवश्यक है।</translation>
    </message>
    <message>
      <source>dialog.color.title</source>
      <translation>रंग</translation>
    </message>
    <message>
      <source>error.autostart.python_unavailable</source>
      <translation>ऑटोस्टार्ट केवल पैकेज्ड EXE में उपलब्ध है। पायथन से चलने पर इसे सक्षम नहीं किया जा सकता है।</translation>
    </message>
    <message>
      <source>error.data.portable_fallback</source>
      <translation>एप्लिकेशन के आगे डेटा नहीं लिखा जा सका. सेटिंग्स अस्थायी रूप से आपके उपयोगकर्ता फ़ोल्डर में संग्रहीत की जाएंगी। पोर्टेबल मोड के लिए, एप्लिकेशन को लिखने योग्य फ़ोल्डर में ले जाएं।</translation>
    </message>
    <message>
      <source>error.data.portable_title</source>
      <translation>पोर्टेबल मोड</translation>
    </message>
    <message>
      <source>error.data.unavailable</source>
      <translation>एप्लिकेशन सेटिंग फ़ोल्डर नहीं बनाया जा सका.</translation>
    </message>
    <message>
      <source>error.widget.hide</source>
      <translation>विजेट छुपाया नहीं जा सका: {error}</translation>
    </message>
    <message>
      <source>error.widget.show</source>
      <translation>विजेट नहीं दिखा सका: {error}</translation>
    </message>
    <message>
      <source>error.widget.state_mismatch</source>
      <translation>विंडो ने अनुरोधित स्थिति में प्रवेश नहीं किया</translation>
    </message>
    <message>
      <source>help.content</source>
      <translation># पोमोडोरो टाइमर

## त्वरित शुरुआत

सेटिंग्स में अवधि चुनें, टाइमर खोलें और **प्रारंभ** चुनें। प्रकाश और अंधेरे मोड के बीच तुरंत परिवर्तन करने के लिए शीर्ष पर स्थित स्विच का उपयोग करें। बाइनरी सेटिंग्स स्विच का उपयोग करती हैं; नियमित क्रियाएँ बटन बनी रहती हैं।

## टाइमर नियंत्रण

- **प्रारंभ** वर्तमान अवधि शुरू करता है।
- **रोकें / जारी रखें** नियमित अवधि को रोकें और फिर से शुरू करें।
- **अवधि छोड़ें** अवधि रिकॉर्ड किए बिना अगले मोड में चला जाता है।
- **रीसेट** रुके हुए कार्य पर लौटता है और सांख्यिकी में रीसेट को रिकॉर्ड करता है।
- **जारी रखें और अगली अवधि शुरू करें** हाथ से अवधि बदलते समय दिखाई देता है, अतिरिक्त समय को एक बार दर्ज करता है और अगली अवधि तुरंत शुरू करता है।

स्वचालित बदलाव में अगली अवधि तुरंत शुरू होती है और कोई अतिरिक्त समय नहीं गिना जाता। हाथ से बदलाव में ऐप **अतिरिक्त काम**, **छोटा विश्राम सीमा से अधिक** या **लंबा विश्राम सीमा से अधिक** दिखाता है और समय से पहले `+` लगाता है। अतिरिक्त समय के दौरान शुरू करें, रोकें, छोड़ें और पुनः आरंभ करें निष्क्रिय रहते हैं, इसलिए कोई समय नष्ट नहीं होता।

## उपस्थिति और पहुंच

धूमकेतु, अरोरा, गर्म और कस्टम थीम में प्रत्येक में प्रकाश और अंधेरे मोड हैं। कस्टम-थीम संपादक मोड को अलग से संग्रहीत करता है, `#RRGGBB` को मान्य करता है, और कंट्रास्ट 4.5:1 से कम होने पर चेतावनी देता है। रद्द करें सहेजे गए रंगों को पुनर्स्थापित करता है; रीसेट सुरक्षित धूमकेतु पैलेट को पुनर्स्थापित करता है।

क्यूटी विजेट्स इंटरफ़ेस विंडोज़/क्यूटी स्केलिंग का अनुसरण करता है और कीबोर्ड फोकस का समर्थन करता है। स्विच माउस, `स्पेस`, या `एंटर` के साथ काम करते हैं; उनकी स्थिति स्थिति, रंग और चालू/बंद पाठ द्वारा बताई जाती है। कमांड बटन `स्पेस` या `एंटर` का भी उपयोग करते हैं, संक्षिप्त प्रेस फीडबैक प्रदान करते हैं, और केवल कीबोर्ड नेविगेशन के दौरान एक उच्च-कंट्रास्ट रूपरेखा दिखाते हैं। जब गति अक्षम हो जाती है, तो तत्काल रंग परिवर्तन एनीमेशन की जगह ले लेता है।

पहले लॉन्च पर, मुख्य विंडो उपलब्ध स्क्रीन का लगभग 80% उपयोग करती है। यह अपने आकार और स्थिति को याद रखता है और रिज़ॉल्यूशन बदलने के बाद दृश्य मॉनिटर पर वापस आ जाता है। मध्यम और संकीर्ण चौड़ाई पर, नेविगेशन टूलटिप्स, बटन ग्रुप रैप और सेटिंग्स स्क्रॉल के साथ आइकन पर पिन किए गए कार्यों को क्लिप किए बिना ढह जाता है।

डार्क मोड व्यूपोर्ट और ट्रे मेनू को स्टाइल करता है और जब Windows DWM इसका समर्थन करता है तो एक डार्क नेटिव टाइटल बार का अनुरोध करता है। मूल टमाटर-और-टाइमर आइकन का उपयोग विंडोज़, टास्कबार, ट्रे और पैकेज्ड EXE के लिए किया जाता है।

## अतिरिक्त समय का संकेत

पल्स, बढ़े हुए अंक, सिग्नल बीकन, एक उच्चारण सीमा, एक तरंग संकेतक, या कोई एनीमेशन नहीं चुनें। रंग परिवर्तन, दायरा, गति, तीव्रता और तीन रंग स्वतंत्र रूप से कॉन्फ़िगर किए गए हैं। पूर्वावलोकन टाइमर, आंकड़े, सूचनाएं या अस्पष्टता को संशोधित नहीं करता है।

मुख्य विंडो और विजेट को समान प्रभाव फ़्रेम प्राप्त होता है। जारी रखें या बाहर निकलें, नियमित रंग और आकार तुरंत बहाल हो जाते हैं। गति अक्षम होने पर, स्थैतिक सुलभ संकेत, राज्य का नाम और `+` चिह्न बना रहता है।

## फ्लोटिंग विजेट

टाइमर पृष्ठ पर **विजेट दिखाएँ** स्विच उसी विंडो को दिखाता और छुपाता है। सात लेआउट उपलब्ध हैं: न्यूनतम, कॉम्पैक्ट, विस्तारित, माइक्रो, पंक्ति, रिंग और स्कोरबोर्ड। सभी एक ही `टाइमरइंजिन` का उपयोग करते हैं।

हर रूप के लिए प्रकार, आकार और स्थान अलग-अलग सहेजे जाते हैं। हाथ से आकार बदलने पर मनपसंद आकार बनता है। अपारदर्शिता 5 से 100% तक होती है; अतिरिक्त समय के दौरान विजेट अस्थायी रूप से पूरी तरह अपारदर्शी हो सकता है और फिर सहेजे गए मान पर लौट आता है।

विस्तारित दृश्य में, एक संकीर्ण क्रिया पट्टी संपूर्ण क्रियाओं को लपेटती है। जारी रखें कभी भी संक्षिप्त नहीं होता। न्यूनतम चौड़ाई पर केवल ओपन टूलटिप वाला आइकन बन सकता है; शेष क्रियाएँ अगली पंक्ति में समाप्त हो जाती हैं।

## सूचनाएं, आंकड़े और ट्रे

स्वचालित बदलाव की सूचना बंद की जा सकती है। हाथ से बदलाव की सूचना में जारी रखें होता है; बंद करें बटन केवल विंडो हटाता है और अतिरिक्त समय सुरक्षित रहता है। वही आदेश मुख्य विंडो और विजेट में उपलब्ध रहते हैं।

आँकड़े आज और पूरे समय के सामान्य काम, सामान्य विश्राम और तीनों अतिरिक्त-समय प्रकारों को अलग रखते हैं। मुख्य विंडो बंद करने पर ऐप सूचना क्षेत्र में छोटा हो सकता है। सामान्य रूप से बाहर निकलने पर जमा अतिरिक्त समय सुरक्षित रहता है।

प्रति विंडोज़ उपयोगकर्ता एक एप्लिकेशन इंस्टेंस चलता है। दूसरा लॉन्च कोई अन्य इंटरफ़ेस बनाए बिना एक सिस्टम संदेश दिखाता है।</translation>
    </message>
    <message>
      <source>help.subtitle</source>
      <translation>सुविधाएँ और सुरक्षित अनुप्रयोग व्यवहार।</translation>
    </message>
    <message>
      <source>help.title</source>
      <translation>मदद</translation>
    </message>
    <message>
      <source>main.brand_subtitle</source>
      <translation>एक शांत कार्य लय</translation>
    </message>
    <message>
      <source>nav.help</source>
      <translation>मदद</translation>
    </message>
    <message>
      <source>nav.settings</source>
      <translation>सेटिंग्स</translation>
    </message>
    <message>
      <source>nav.statistics</source>
      <translation>आंकड़े</translation>
    </message>
    <message>
      <source>nav.timer</source>
      <translation>घड़ी</translation>
    </message>
    <message>
      <source>notification.auto_transition</source>
      <translation>{completed}

अगली अवधि पहले ही शुरू हो चुकी है: {next_period}।</translation>
    </message>
    <message>
      <source>notification.completed.long_break</source>
      <translation>लंबा विश्राम पूरा हुआ।</translation>
    </message>
    <message>
      <source>notification.completed.short_break</source>
      <translation>छोटा विश्राम पूरा हुआ।</translation>
    </message>
    <message>
      <source>notification.completed.work</source>
      <translation>कार्य अवधि पूरी हुई।</translation>
    </message>
    <message>
      <source>notification.default.long_break_end</source>
      <translation>लंबा विश्राम पूरा हुआ। नई कार्य अवधि शुरू करने का समय है।</translation>
    </message>
    <message>
      <source>notification.default.short_break_end</source>
      <translation>छोटा विश्राम पूरा हुआ। काम पर लौटने का समय है।</translation>
    </message>
    <message>
      <source>notification.default.work_end</source>
      <translation>कार्य अवधि पूरी हुई। अब विश्राम का समय है।</translation>
    </message>
    <message>
      <source>notification.manual_transition</source>
      <translation>{completed}

{next_period} प्रारंभ करने के लिए जारी रखें का चयन करें।</translation>
    </message>
    <message>
      <source>overrun.effect.beacons</source>
      <translation>चेतावनी संकेत</translation>
    </message>
    <message>
      <source>overrun.effect.border</source>
      <translation>उभरी सीमा</translation>
    </message>
    <message>
      <source>overrun.effect.none</source>
      <translation>बिना गति प्रभाव</translation>
    </message>
    <message>
      <source>overrun.effect.pulse</source>
      <translation>स्पंदन</translation>
    </message>
    <message>
      <source>overrun.effect.scale</source>
      <translation>अंक बढ़ाएँ</translation>
    </message>
    <message>
      <source>overrun.effect.wave</source>
      <translation>तरंग सूचक</translation>
    </message>
    <message>
      <source>overrun.intensity.medium</source>
      <translation>मध्यम</translation>
    </message>
    <message>
      <source>overrun.intensity.strong</source>
      <translation>प्रबल</translation>
    </message>
    <message>
      <source>overrun.intensity.weak</source>
      <translation>हल्का</translation>
    </message>
    <message>
      <source>overrun.scope.both</source>
      <translation>अंक और समय-पट्ट</translation>
    </message>
    <message>
      <source>overrun.scope.card</source>
      <translation>समय-पट्ट</translation>
    </message>
    <message>
      <source>overrun.scope.digits</source>
      <translation>केवल समय के अंक</translation>
    </message>
    <message>
      <source>overrun.speed.fast</source>
      <translation>तेज़</translation>
    </message>
    <message>
      <source>overrun.speed.normal</source>
      <translation>सामान्य</translation>
    </message>
    <message>
      <source>overrun.speed.slow</source>
      <translation>धीमा</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode</source>
      <translation>गहरा रूप</translation>
    </message>
    <message>
      <source>settings.appearance.dark_mode.description</source>
      <translation>बंद - लाइट मोड, चालू - डार्क मोड।</translation>
    </message>
    <message>
      <source>settings.appearance.edit_colors</source>
      <translation>रंग अनुकूलित करें</translation>
    </message>
    <message>
      <source>settings.appearance.editor_unavailable</source>
      <translation>इस विंडो में संपादक उपलब्ध नहीं है.</translation>
    </message>
    <message>
      <source>settings.appearance.language</source>
      <translation>इंटरफ़ेस भाषा</translation>
    </message>
    <message>
      <source>settings.appearance.subtitle</source>
      <translation>पूर्ण पैलेट प्रत्येक खुली हुई विंडो को पुनः आरंभ किए बिना अद्यतन करते हैं।</translation>
    </message>
    <message>
      <source>settings.appearance.title</source>
      <translation>उपस्थिति</translation>
    </message>
    <message>
      <source>settings.logic.long_break_interval</source>
      <translation>लंबे विश्राम से पहले कार्य अवधियाँ</translation>
    </message>
    <message>
      <source>settings.logic.subtitle</source>
      <translation>काम, छोटे विश्राम और लंबे विश्राम का क्रम।</translation>
    </message>
    <message>
      <source>settings.logic.title</source>
      <translation>टाइमर व्यवहार</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break</source>
      <translation>लंबे विश्राम का उपयोग करें</translation>
    </message>
    <message>
      <source>settings.logic.use_long_break.description</source>
      <translation>कार्य अवधि की निर्दिष्ट संख्या के बाद.</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition</source>
      <translation>स्वचालित संक्रमण</translation>
    </message>
    <message>
      <source>settings.notifications.auto_transition.description</source>
      <translation>चालू — अगली अवधि तुरंत शुरू होती है; बंद — अतिरिक्त समय गिना जाता है।</translation>
    </message>
    <message>
      <source>settings.notifications.enabled</source>
      <translation>सूचनाएं</translation>
    </message>
    <message>
      <source>settings.notifications.long_break_end</source>
      <translation>लंबा विश्राम पूरा होना</translation>
    </message>
    <message>
      <source>settings.notifications.short_break_end</source>
      <translation>अल्प विराम समापन</translation>
    </message>
    <message>
      <source>settings.notifications.sound</source>
      <translation>अधिसूचना ध्वनि</translation>
    </message>
    <message>
      <source>settings.notifications.subtitle</source>
      <translation>मैन्युअल ट्रांज़िशन हमेशा मुख्य विंडो या विजेट से पूरा किया जा सकता है।</translation>
    </message>
    <message>
      <source>settings.notifications.title</source>
      <translation>सूचनाएं</translation>
    </message>
    <message>
      <source>settings.notifications.work_end</source>
      <translation>कार्य पूर्णता</translation>
    </message>
    <message>
      <source>settings.overrun.allow_motion</source>
      <translation>प्रभाव गति की अनुमति दें</translation>
    </message>
    <message>
      <source>settings.overrun.change_color</source>
      <translation>टाइमर का रंग बदलें</translation>
    </message>
    <message>
      <source>settings.overrun.color_dialog</source>
      <translation>अतिरंजित रंग</translation>
    </message>
    <message>
      <source>settings.overrun.effect</source>
      <translation>प्राथमिक प्रभाव</translation>
    </message>
    <message>
      <source>settings.overrun.intensity</source>
      <translation>तीव्रता</translation>
    </message>
    <message>
      <source>settings.overrun.invalid_colors</source>
      <translation>अमान्य रंगों को सक्रिय थीम के मानों से बदल दिया गया।</translation>
    </message>
    <message>
      <source>settings.overrun.opaque_widget</source>
      <translation>अतिरिक्त समय के दौरान विजेट को अपारदर्शी रखें</translation>
    </message>
    <message>
      <source>settings.overrun.scope</source>
      <translation>रंग परिवर्तन क्षेत्र</translation>
    </message>
    <message>
      <source>settings.overrun.separate_colors</source>
      <translation>अलग रंग</translation>
    </message>
    <message>
      <source>settings.overrun.speed</source>
      <translation>रफ़्तार</translation>
    </message>
    <message>
      <source>settings.overrun.subtitle</source>
      <translation>एक साझा फ़्रेम मुख्य विंडो और खुले विजेट पर लगाया जाता है।</translation>
    </message>
    <message>
      <source>settings.overrun.title</source>
      <translation>अतिरिक्त समय संकेत</translation>
    </message>
    <message>
      <source>settings.overrun.use_theme_color</source>
      <translation>थीम रंग का प्रयोग करें</translation>
    </message>
    <message>
      <source>settings.profiles.apply</source>
      <translation>प्रोफ़ाइल लागू करें</translation>
    </message>
    <message>
      <source>settings.profiles.default_cannot_delete</source>
      <translation>डिफ़ॉल्ट प्रोफ़ाइल को हटाया नहीं जा सकता.</translation>
    </message>
    <message>
      <source>settings.profiles.default_name</source>
      <translation>गलती करना</translation>
    </message>
    <message>
      <source>settings.profiles.defaults</source>
      <translation>न्यूनता समायोजन</translation>
    </message>
    <message>
      <source>settings.profiles.delete</source>
      <translation>प्रोफ़ाइल हटाएं</translation>
    </message>
    <message>
      <source>settings.profiles.delete_confirmation</source>
      <translation>प्रोफ़ाइल "{profile_name}" हटाएं?</translation>
    </message>
    <message>
      <source>settings.profiles.delete_title</source>
      <translation>प्रोफ़ाइल हटाएं</translation>
    </message>
    <message>
      <source>settings.profiles.dialog_title</source>
      <translation>प्रोफ़ाइल</translation>
    </message>
    <message>
      <source>settings.profiles.enter_name</source>
      <translation>प्रोफ़ाइल नाम दर्ज करें.</translation>
    </message>
    <message>
      <source>settings.profiles.name_placeholder</source>
      <translation>प्रोफ़ाइल नाम</translation>
    </message>
    <message>
      <source>settings.profiles.restore_personal</source>
      <translation>मेरी सेटिंग्स पुनर्स्थापित करें</translation>
    </message>
    <message>
      <source>settings.profiles.save</source>
      <translation>प्रोफ़ाइल बचा</translation>
    </message>
    <message>
      <source>settings.profiles.select_profile</source>
      <translation>सूची से एक प्रोफ़ाइल चुनें.</translation>
    </message>
    <message>
      <source>settings.profiles.subtitle</source>
      <translation>अवधि, उपस्थिति विकल्प और विजेट सेटिंग्स के सेट सहेजें।</translation>
    </message>
    <message>
      <source>settings.profiles.title</source>
      <translation>प्रोफाइल</translation>
    </message>
    <message>
      <source>settings.save</source>
      <translation>सेटिंग्स सेव करें</translation>
    </message>
    <message>
      <source>settings.section.appearance</source>
      <translation>उपस्थिति</translation>
    </message>
    <message>
      <source>settings.section.logic</source>
      <translation>टाइमर व्यवहार</translation>
    </message>
    <message>
      <source>settings.section.notifications</source>
      <translation>सूचनाएं</translation>
    </message>
    <message>
      <source>settings.section.overrun</source>
      <translation>अतिरिक्त समय</translation>
    </message>
    <message>
      <source>settings.section.profiles</source>
      <translation>प्रोफाइल</translation>
    </message>
    <message>
      <source>settings.section.time</source>
      <translation>समय</translation>
    </message>
    <message>
      <source>settings.section.tray</source>
      <translation>ट्रे और ऑटोस्टार्ट</translation>
    </message>
    <message>
      <source>settings.section.widget</source>
      <translation>विजेट</translation>
    </message>
    <message>
      <source>settings.subtitle</source>
      <translation>थीम और विजेट परिवर्तन तुरंत लागू होते हैं; अन्य परिवर्तन सहेजने के बाद लागू होते हैं.</translation>
    </message>
    <message>
      <source>settings.time.format</source>
      <translation>समय स्वरूप</translation>
    </message>
    <message>
      <source>settings.time.long_break_minutes</source>
      <translation>लंबा विश्राम, मिनट</translation>
    </message>
    <message>
      <source>settings.time.short_break_minutes</source>
      <translation>छोटा विश्राम, मिनट</translation>
    </message>
    <message>
      <source>settings.time.subtitle</source>
      <translation>जब आप बचत करते हैं तो अवधियाँ सुरक्षित रूप से लागू होती हैं।</translation>
    </message>
    <message>
      <source>settings.time.title</source>
      <translation>समय</translation>
    </message>
    <message>
      <source>settings.time.work_minutes</source>
      <translation>कार्य, मिनट</translation>
    </message>
    <message>
      <source>settings.title</source>
      <translation>सेटिंग्स</translation>
    </message>
    <message>
      <source>settings.tray.autostart</source>
      <translation>विंडो के साथ शुरू करें</translation>
    </message>
    <message>
      <source>settings.tray.autostart_current</source>
      <translation>ऑटोस्टार्ट सक्षम है और एप्लिकेशन के वर्तमान फ़ोल्डर को इंगित करता है।</translation>
    </message>
    <message>
      <source>settings.tray.autostart_disabled</source>
      <translation>ऑटोस्टार्ट अक्षम है.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_python</source>
      <translation>पायथन से चल रहा है: ऑटोस्टार्ट को EXE संस्करण में सक्षम किया जा सकता है।</translation>
    </message>
    <message>
      <source>settings.tray.autostart_stale</source>
      <translation>ऑटोस्टार्ट पथ पुराना है. एप्लिकेशन को स्थानांतरित करने के बाद इसे अपडेट करें.</translation>
    </message>
    <message>
      <source>settings.tray.autostart_title</source>
      <translation>ऑटो स्टार्ट</translation>
    </message>
    <message>
      <source>settings.tray.close_to_tray</source>
      <translation>बंद करते समय ट्रे को छोटा करें</translation>
    </message>
    <message>
      <source>settings.tray.minimize_on_start</source>
      <translation>लॉन्च के बाद एप्लिकेशन को छोटा करें</translation>
    </message>
    <message>
      <source>settings.tray.subtitle</source>
      <translation>सिस्टम ट्रे साझा Qt GUI थ्रेड में चलता है।</translation>
    </message>
    <message>
      <source>settings.tray.title</source>
      <translation>ट्रे और ऑटोस्टार्ट</translation>
    </message>
    <message>
      <source>settings.tray.update_autostart</source>
      <translation>ऑटोस्टार्ट पथ अपडेट करें</translation>
    </message>
    <message>
      <source>settings.widget.always_on_top</source>
      <translation>हमेशा ऊपर</translation>
    </message>
    <message>
      <source>settings.widget.dialog_title</source>
      <translation>विजेट</translation>
    </message>
    <message>
      <source>settings.widget.opacity</source>
      <translation>विजेट अपारदर्शिता</translation>
    </message>
    <message>
      <source>settings.widget.opacity.description</source>
      <translation>कम मान विजेट को अधिक पारदर्शी बनाते हैं। न्यूनतम - 5%।</translation>
    </message>
    <message>
      <source>settings.widget.position_reset</source>
      <translation>वर्तमान प्रकार की स्थिति रीसेट कर दी गई है.</translation>
    </message>
    <message>
      <source>settings.widget.reset_position</source>
      <translation>वर्तमान प्रकार के लिए स्थिति रीसेट करें</translation>
    </message>
    <message>
      <source>settings.widget.size</source>
      <translation>आकार</translation>
    </message>
    <message>
      <source>settings.widget.subtitle</source>
      <translation>दृश्यता को टाइमर पृष्ठ पर स्विच द्वारा नियंत्रित किया जाता है।</translation>
    </message>
    <message>
      <source>settings.widget.title</source>
      <translation>फ़्लोटिंग विजेट</translation>
    </message>
    <message>
      <source>settings.widget.type</source>
      <translation>विजेट प्रकार</translation>
    </message>
    <message>
      <source>startup.already_running</source>
      <translation>पोमोडोरो टाइमर प्रारंभ हो रहा है या पहले से ही चल रहा है। विंडो खुलने तक प्रतीक्षा करें या पहले से खुले एप्लिकेशन का उपयोग करें।</translation>
    </message>
    <message>
      <source>startup.lock.already_running</source>
      <translation>एक अन्य एप्लिकेशन इंस्टेंस पहले से ही चल रहा है।</translation>
    </message>
    <message>
      <source>startup.lock.create_failed</source>
      <translation>सिस्टम लॉक नहीं बनाया जा सका (WinError {error_code})।</translation>
    </message>
    <message>
      <source>startup.lock.release_failed</source>
      <translation>सिस्टम लॉक जारी नहीं किया जा सका (WinError {error_code})।</translation>
    </message>
    <message>
      <source>startup.lock.secondary_close_failed</source>
      <translation>एक अन्य उदाहरण पहले से ही चल रहा है, लेकिन इसका द्वितीयक हैंडल बंद नहीं किया जा सका (WinError {error_code})।</translation>
    </message>
    <message>
      <source>startup.lock.unsupported</source>
      <translation>सिंगल-इंस्टेंस सिस्टम लॉक केवल विंडोज़ पर समर्थित है।</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_cycles</source>
      <translation>
        <numerusform>पूरा चक्र</numerusform>
        <numerusform>पूर्ण चक्र</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_long_breaks</source>
      <translation>
        <numerusform>लंबा विश्राम</numerusform>
        <numerusform>लंबे विश्राम</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_short_breaks</source>
      <translation>
        <numerusform>छोटा विश्राम</numerusform>
        <numerusform>छोटे विश्राम</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.completed_work_periods</source>
      <translation>
        <numerusform>कार्य अवधि</numerusform>
        <numerusform>कार्य अवधि</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.long_break_overrun</source>
      <translation>लंबा विश्राम सीमा से अधिक</translation>
    </message>
    <message>
      <source>stats.metric.overwork_time</source>
      <translation>अतिरिक्त काम का समय</translation>
    </message>
    <message>
      <source>stats.metric.rest_time</source>
      <translation>विराम समय</translation>
    </message>
    <message>
      <source>stats.metric.short_break_overrun</source>
      <translation>छोटा विश्राम सीमा से अधिक</translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.skipped_periods</source>
      <translation>
        <numerusform>छोड़ी गई अवधि</numerusform>
        <numerusform>छूटे हुए पीरियड्स</numerusform>
      </translation>
    </message>
    <message numerus="yes">
      <source>stats.metric.timer_resets</source>
      <translation>
        <numerusform>टाइमर रीसेट</numerusform>
        <numerusform>टाइमर रीसेट</numerusform>
      </translation>
    </message>
    <message>
      <source>stats.metric.work_time</source>
      <translation>काम का समय</translation>
    </message>
    <message>
      <source>stats.period.all_time</source>
      <translation>पूरे समय</translation>
    </message>
    <message>
      <source>stats.period.today</source>
      <translation>आज</translation>
    </message>
    <message>
      <source>stats.reset.action</source>
      <translation>सांख्यिकीय को रीसेट करें</translation>
    </message>
    <message>
      <source>stats.reset.confirmation</source>
      <translation>क्या आप वाकई सभी आँकड़े हटाना चाहते हैं?</translation>
    </message>
    <message>
      <source>stats.reset.title</source>
      <translation>सांख्यिकीय को रीसेट करें</translation>
    </message>
    <message>
      <source>stats.subtitle</source>
      <translation>सामान्य और अतिरिक्त समय अलग-अलग दर्ज होते हैं।</translation>
    </message>
    <message>
      <source>stats.title</source>
      <translation>आंकड़े</translation>
    </message>
    <message>
      <source>theme.appearance.dark</source>
      <translation>गहरा</translation>
    </message>
    <message>
      <source>theme.appearance.light</source>
      <translation>हल्का</translation>
    </message>
    <message>
      <source>theme.contrast.accent</source>
      <translation>उच्चारण पाठ/उच्चारण</translation>
    </message>
    <message>
      <source>theme.contrast.button</source>
      <translation>बटन टेक्स्ट/बटन</translation>
    </message>
    <message>
      <source>theme.contrast.long_break</source>
      <translation>लंबा विश्राम / पटल</translation>
    </message>
    <message>
      <source>theme.contrast.long_break_overrun</source>
      <translation>लंबा विश्राम सीमा से अधिक / पटल</translation>
    </message>
    <message>
      <source>theme.contrast.overwork</source>
      <translation>अतिरिक्त काम / पटल</translation>
    </message>
    <message>
      <source>theme.contrast.primary_card</source>
      <translation>प्राथमिक पाठ/कार्ड</translation>
    </message>
    <message>
      <source>theme.contrast.secondary_card</source>
      <translation>द्वितीयक पाठ/कार्ड</translation>
    </message>
    <message>
      <source>theme.contrast.short_break</source>
      <translation>छोटा विश्राम / पटल</translation>
    </message>
    <message>
      <source>theme.contrast.short_break_overrun</source>
      <translation>छोटा विश्राम सीमा से अधिक / पटल</translation>
    </message>
    <message>
      <source>theme.contrast.work</source>
      <translation>कार्य/कार्ड</translation>
    </message>
    <message>
      <source>theme.description.aurora</source>
      <translation>शानदार नीला और बैंगनी लहजा</translation>
    </message>
    <message>
      <source>theme.description.comet</source>
      <translation>शांत तटस्थ पैलेट</translation>
    </message>
    <message>
      <source>theme.description.custom</source>
      <translation>आपके स्वतंत्र प्रकाश और अंधेरे पैलेट</translation>
    </message>
    <message>
      <source>theme.description.warm</source>
      <translation>नरम रेतीली और गर्म सतहें</translation>
    </message>
    <message>
      <source>theme.name.aurora</source>
      <translation>अरोड़ा</translation>
    </message>
    <message>
      <source>theme.name.comet</source>
      <translation>कोमेट</translation>
    </message>
    <message>
      <source>theme.name.custom</source>
      <translation>मनपसंद</translation>
    </message>
    <message>
      <source>theme.name.warm</source>
      <translation>गरम</translation>
    </message>
    <message>
      <source>theme_editor.color.accent</source>
      <translation>लहज़ा</translation>
    </message>
    <message>
      <source>theme_editor.color.accent_hover</source>
      <translation>मंडराना</translation>
    </message>
    <message>
      <source>theme_editor.color.background</source>
      <translation>मुख्य पृष्ठभूमि</translation>
    </message>
    <message>
      <source>theme_editor.color.border</source>
      <translation>सीमाएँ</translation>
    </message>
    <message>
      <source>theme_editor.color.button_background</source>
      <translation>बटन का रंग</translation>
    </message>
    <message>
      <source>theme_editor.color.button_text</source>
      <translation>बटन पाठ</translation>
    </message>
    <message>
      <source>theme_editor.color.card_background</source>
      <translation>कार्ड पृष्ठभूमि</translation>
    </message>
    <message>
      <source>theme_editor.color.disabled</source>
      <translation>अक्षम तत्व</translation>
    </message>
    <message>
      <source>theme_editor.color.error</source>
      <translation>गलती</translation>
    </message>
    <message>
      <source>theme_editor.color.focus</source>
      <translation>केंद्र</translation>
    </message>
    <message>
      <source>theme_editor.color.on_accent</source>
      <translation>एक्सेंट बटन टेक्स्ट</translation>
    </message>
    <message>
      <source>theme_editor.color.secondary_background</source>
      <translation>द्वितीयक पृष्ठभूमि</translation>
    </message>
    <message>
      <source>theme_editor.color.success</source>
      <translation>सफलता</translation>
    </message>
    <message>
      <source>theme_editor.color.text_primary</source>
      <translation>प्राथमिक पाठ</translation>
    </message>
    <message>
      <source>theme_editor.color.text_secondary</source>
      <translation>द्वितीयक पाठ</translation>
    </message>
    <message>
      <source>theme_editor.color.warning</source>
      <translation>चेतावनी</translation>
    </message>
    <message>
      <source>theme_editor.contrast.ok</source>
      <translation>कंट्रास्ट जांच: मुख्य संयोजन 4.5:1 दिशानिर्देश को पूरा करते हैं।</translation>
    </message>
    <message numerus="yes">
      <source>theme_editor.contrast.warning</source>
      <translation>
        <numerusform>कंट्रास्ट जांच: {count} संयोजन 4.5:1 से नीचे है। आवेदन करते समय पुष्टि की आवश्यकता होगी।</numerusform>
        <numerusform>कंट्रास्ट जांच: {count} संयोजन 4.5:1 से नीचे हैं। आवेदन करते समय पुष्टि की आवश्यकता होगी।</numerusform>
      </translation>
    </message>
    <message>
      <source>theme_editor.create_copy</source>
      <translation>प्रति बनाएँ</translation>
    </message>
    <message>
      <source>theme_editor.create_from</source>
      <translation>से बनाएं</translation>
    </message>
    <message>
      <source>theme_editor.editing_mode</source>
      <translation>मोड संपादित किया जा रहा है</translation>
    </message>
    <message>
      <source>theme_editor.group.service_states</source>
      <translation>स्थिति रंग</translation>
    </message>
    <message>
      <source>theme_editor.group.surfaces</source>
      <translation>सतह</translation>
    </message>
    <message>
      <source>theme_editor.group.text_controls</source>
      <translation>पाठ और नियंत्रण</translation>
    </message>
    <message>
      <source>theme_editor.group.timer_states</source>
      <translation>टाइमर बताता है</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.confirmation</source>
      <translation>कुछ संयोजन 4.5:1 से नीचे हैं:

{details}

फिर भी बचाएं?</translation>
    </message>
    <message>
      <source>theme_editor.low_contrast.title</source>
      <translation>कम कंट्रास्ट</translation>
    </message>
    <message>
      <source>theme_editor.reset.confirmation</source>
      <translation>दोनों मोड को सुरक्षित धूमकेतु थीम पर रीसेट करें?</translation>
    </message>
    <message>
      <source>theme_editor.reset.title</source>
      <translation>थीम रीसेट करें</translation>
    </message>
    <message>
      <source>theme_editor.reset_all</source>
      <translation>संपूर्ण थीम रीसेट करें</translation>
    </message>
    <message>
      <source>theme_editor.reset_mode</source>
      <translation>वर्तमान मोड रीसेट करें</translation>
    </message>
    <message>
      <source>theme_editor.subtitle</source>
      <translation>प्रकाश और अंधेरे मोड को स्वतंत्र रूप से संपादित करें।</translation>
    </message>
    <message>
      <source>theme_editor.title</source>
      <translation>कस्टम थीम</translation>
    </message>
    <message>
      <source>timer.mode.long_break</source>
      <translation>लंबा विश्राम</translation>
    </message>
    <message>
      <source>timer.mode.long_break_overrun</source>
      <translation>लंबा विश्राम सीमा से अधिक</translation>
    </message>
    <message>
      <source>timer.mode.overwork</source>
      <translation>अतिरिक्त काम</translation>
    </message>
    <message>
      <source>timer.mode.short_break</source>
      <translation>छोटा विश्राम</translation>
    </message>
    <message>
      <source>timer.mode.short_break_overrun</source>
      <translation>छोटा विश्राम सीमा से अधिक</translation>
    </message>
    <message>
      <source>timer.mode.work</source>
      <translation>काम</translation>
    </message>
    <message>
      <source>timer.overrun.waiting_status</source>
      <translation>अवधि पूरी हुई — जारी रखने तक अतिरिक्त समय गिना जाएगा</translation>
    </message>
    <message>
      <source>timer.page.subtitle</source>
      <translation>मुख्य विंडो, सूचनाओं और विजेट के लिए एक टाइमर।</translation>
    </message>
    <message>
      <source>timer.page.title</source>
      <translation>फोकस सत्र</translation>
    </message>
    <message>
      <source>timer.status.accessible_name</source>
      <translation>टाइमर स्थिति</translation>
    </message>
    <message>
      <source>timer.status.overrun</source>
      <translation>अतिरिक्त समय गिना जा रहा है</translation>
    </message>
    <message>
      <source>timer.status.paused</source>
      <translation>टाइमर रुक गया</translation>
    </message>
    <message>
      <source>timer.status.running</source>
      <translation>टाइमर चल रहा है</translation>
    </message>
    <message>
      <source>timer.status.stopped</source>
      <translation>टाइमर बंद हो गया</translation>
    </message>
    <message>
      <source>timer.widget.show</source>
      <translation>विजेट दिखाएँ</translation>
    </message>
    <message>
      <source>timer.widget.show.description</source>
      <translation>स्थिति, आकार, प्रकार और अपारदर्शिता अलग-अलग सहेजी जाती हैं।</translation>
    </message>
    <message>
      <source>toggle.accessible_description</source>
      <translation>चालू - सक्षम, बंद - अक्षम</translation>
    </message>
    <message>
      <source>toggle.accessible_name</source>
      <translation>बदलना</translation>
    </message>
    <message>
      <source>toggle.off</source>
      <translation>बंद</translation>
    </message>
    <message>
      <source>toggle.on</source>
      <translation>पर</translation>
    </message>
    <message>
      <source>toggle.state.off</source>
      <translation>बंद, अक्षम</translation>
    </message>
    <message>
      <source>toggle.state.on</source>
      <translation>चालू, सक्षम</translation>
    </message>
    <message>
      <source>tray.exit</source>
      <translation>बाहर निकलें</translation>
    </message>
    <message>
      <source>tray.hide</source>
      <translation>विंडो छिपाएँ</translation>
    </message>
    <message>
      <source>tray.reset</source>
      <translation>पुनः आरंभ करें</translation>
    </message>
    <message>
      <source>tray.show</source>
      <translation>विंडो दिखाएँ</translation>
    </message>
    <message>
      <source>tray.start_pause</source>
      <translation>शुरू करें / रोकें</translation>
    </message>
    <message numerus="yes">
      <source>widget.completed_work_periods</source>
      <translation>
        <numerusform>पूर्ण कार्य अवधि: {count}</numerusform>
        <numerusform>पूर्ण कार्य अवधि: {count}</numerusform>
      </translation>
    </message>
    <message>
      <source>widget.size.custom</source>
      <translation>मनपसंद</translation>
    </message>
    <message>
      <source>widget.size.large</source>
      <translation>बड़ा</translation>
    </message>
    <message>
      <source>widget.size.medium</source>
      <translation>मध्यम</translation>
    </message>
    <message>
      <source>widget.size.small</source>
      <translation>छोटा</translation>
    </message>
    <message>
      <source>widget.type.compact</source>
      <translation>सघन</translation>
    </message>
    <message>
      <source>widget.type.compact.description</source>
      <translation>प्राथमिक क्रिया के साथ एक क्लासिक कॉम्पैक्ट कार्ड।</translation>
    </message>
    <message>
      <source>widget.type.expanded</source>
      <translation>विस्तारित</translation>
    </message>
    <message>
      <source>widget.type.expanded.description</source>
      <translation>चक्र की जानकारी और प्राथमिक टाइमर क्रियाओं का पूरा सेट।</translation>
    </message>
    <message>
      <source>widget.type.micro</source>
      <translation>सूक्ष्म</translation>
    </message>
    <message>
      <source>widget.type.micro.description</source>
      <translation>सबसे छोटी खिड़की: आमतौर पर सिर्फ समय।</translation>
    </message>
    <message>
      <source>widget.type.minimal</source>
      <translation>न्यूनतम</translation>
    </message>
    <message>
      <source>widget.type.minimal.description</source>
      <translation>बड़ा समय, राज्य का नाम और न्यूनतम विवरण।</translation>
    </message>
    <message>
      <source>widget.type.ring</source>
      <translation>वृत्ताकार</translation>
    </message>
    <message>
      <source>widget.type.ring.description</source>
      <translation>एक वृत्ताकार अवधि सूचक के अंदर का समय.</translation>
    </message>
    <message>
      <source>widget.type.row</source>
      <translation>पंक्ति</translation>
    </message>
    <message>
      <source>widget.type.row.description</source>
      <translation>स्क्रीन के किनारे के लिए एक क्षैतिज पंक्ति.</translation>
    </message>
    <message>
      <source>widget.type.scoreboard</source>
      <translation>अंक-पट्ट</translation>
    </message>
    <message>
      <source>widget.type.scoreboard.description</source>
      <translation>शांत स्कोरबोर्ड शैली में बड़े मोनोस्पेस्ड अंक।</translation>
    </message>
    <message>
      <source>widget.window_title</source>
      <translation>पोमोडोरो विजेट</translation>
    </message>
  </context>
  <context>
    <name>QPlatformTheme</name>
    <message>
      <source>OK</source>
      <translation>ठीक है</translation>
    </message>
    <message>
      <source>Save</source>
      <translation>सहेजें</translation>
    </message>
    <message>
      <source>Save All</source>
      <translation>सभी सहेजें</translation>
    </message>
    <message>
      <source>Open</source>
      <translation>खोलें</translation>
    </message>
    <message>
      <source>&amp;Yes</source>
      <translation>&amp;हाँ</translation>
    </message>
    <message>
      <source>Yes to &amp;All</source>
      <translation>सभी के लिए &amp;हाँ</translation>
    </message>
    <message>
      <source>&amp;No</source>
      <translation>&amp;नहीं</translation>
    </message>
    <message>
      <source>N&amp;o to All</source>
      <translation>सभी के लिए न&amp;हीं</translation>
    </message>
    <message>
      <source>Abort</source>
      <translation>रद्द करें</translation>
    </message>
    <message>
      <source>Retry</source>
      <translation>पुनः प्रयास करें</translation>
    </message>
    <message>
      <source>Ignore</source>
      <translation>अनदेखा करें</translation>
    </message>
    <message>
      <source>Close</source>
      <translation>बंद करें</translation>
    </message>
    <message>
      <source>Cancel</source>
      <translation>रद्द करें</translation>
    </message>
    <message>
      <source>Discard</source>
      <translation>परिवर्तन छोड़ें</translation>
    </message>
    <message>
      <source>Help</source>
      <translation>सहायता</translation>
    </message>
    <message>
      <source>Apply</source>
      <translation>लागू करें</translation>
    </message>
    <message>
      <source>Reset</source>
      <translation>रीसेट करें</translation>
    </message>
    <message>
      <source>Restore Defaults</source>
      <translation>डिफ़ॉल्ट मान पुनर्स्थापित करें</translation>
    </message>
  </context>
</TS>
