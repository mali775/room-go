import 'dart:html' as html;
import 'package:flutter/material.dart';
import 'dart:ui_web' as ui_web;

Widget buildMapView(String url) {
  final String viewId = 'iframeElement_${url.hashCode}';
  
  // Register the factory only once per URL
  ui_web.platformViewRegistry.registerViewFactory(
    viewId,
    (int viewId) => html.IFrameElement()
      ..src = url
      ..style.border = 'none'
      ..style.width = '100%'
      ..style.height = '100%'
  );

  return HtmlElementView(viewType: viewId);
}
