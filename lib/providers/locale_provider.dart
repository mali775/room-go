import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../l10n/app_translations.dart';

class LocaleProvider extends ChangeNotifier {
  String _currentLocale = 'kk';

  String get currentLocale => _currentLocale;

  LocaleProvider() {
    _loadLocale();
  }

  void _loadLocale() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    _currentLocale = prefs.getString('locale') ?? 'kk';
    notifyListeners();
  }

  void setLocale(String locale) async {
    if (_currentLocale != locale) {
      _currentLocale = locale;
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.setString('locale', locale);
      notifyListeners();
    }
  }

  String translate(String key) {
    return translations[_currentLocale]?[key] ?? key;
  }
}
