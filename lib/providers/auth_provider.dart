import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/database_service.dart';

class AuthProvider extends ChangeNotifier {
  bool _isAuthenticated = false;
  String? _currentUserEmail;
  String? _currentUserName;

  bool get isAuthenticated => _isAuthenticated;
  String? get currentUserEmail => _currentUserEmail;
  String get displayName {
    if (_currentUserName != null && _currentUserName!.isNotEmpty) {
      return _currentUserName!;
    }
    if (_currentUserEmail != null && _currentUserEmail!.isNotEmpty) {
      final prefix = _currentUserEmail!.split('@').first;
      return prefix.isNotEmpty ? '${prefix[0].toUpperCase()}${prefix.substring(1)}' : 'Student';
    }
    return 'Student';
  }

  AuthProvider() {
    _loadAuthStatus();
  }

  void _loadAuthStatus() async {
    final prefs = await SharedPreferences.getInstance();
    _isAuthenticated = prefs.getBool('is_authenticated') ?? false;
    _currentUserEmail = prefs.getString('user_email');
    _currentUserName = prefs.getString('user_name');
    notifyListeners();
  }

  Future<bool> login(String email, String password) async {
    final trimmedEmail = email.trim();
    if (trimmedEmail.isEmpty || password.isEmpty) return false;

    try {
      final success = await DatabaseService.loginUser(trimmedEmail, password);
      if (success) {
        _isAuthenticated = true;
        _currentUserEmail = trimmedEmail;
        _currentUserName = trimmedEmail.split('@').first;

        final prefs = await SharedPreferences.getInstance();
        await prefs.setBool('is_authenticated', true);
        await prefs.setString('user_email', trimmedEmail);
        await prefs.setString('user_name', _currentUserName!);

        notifyListeners();
        return true;
      }
    } catch (e) {
      debugPrint('Login exception: $e');
    }
    return false;
  }

  Future<bool> register(String email, String password) async {
    final trimmedEmail = email.trim();
    if (trimmedEmail.isEmpty || password.length < 6) return false;

    try {
      final success = await DatabaseService.registerUser(trimmedEmail, password);
      if (success) {
        return true;
      }
    } catch (e) {
      debugPrint('Register exception: $e');
    }
    return false;
  }

  Future<void> logout() async {
    _isAuthenticated = false;
    _currentUserEmail = null;
    _currentUserName = null;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('is_authenticated');
    await prefs.remove('user_email');
    await prefs.remove('user_name');

    notifyListeners();
  }
}
