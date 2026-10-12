import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

Widget buildMapView(String url) {
  return Center(
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(Icons.map_rounded, size: 80, color: const Color(0xFF94A3B8)),
        SizedBox(height: 24),
        Text(
          'Map View',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.w800,
            color: const Color(0xFF0F172A),
          ),
        ),
        SizedBox(height: 16),
        Text(
          'Interactive map is available in browser.',
          style: TextStyle(color: const Color(0xFF64748B)),
        ),
        SizedBox(height: 24),
        ElevatedButton.icon(
          onPressed: () async {
            final uri = Uri.parse(url);
            if (await canLaunchUrl(uri)) {
              await launchUrl(uri);
            }
          },
          icon: Icon(Icons.open_in_new_rounded),
          label: Text('Open in Browser'),
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFF2563EB),
            foregroundColor: Colors.white,
          ),
        ),
      ],
    ),
  );
}
