# GruhaAlankar Flutter Integration Guide

**Quick Reference for Flutter Developers**

---

## Setup

### 1. Add Dependencies to `pubspec.yaml`

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  provider: ^6.0.0
  image_picker: ^1.0.0
  model_viewer: ^1.0.0  # For 3D model viewing
  cached_network_image: ^3.0.0
  hive: ^2.0.0  # For local storage
  hive_flutter: ^1.0.0
```

### 2. Constants File

```dart
// lib/constants/api_constants.dart
class ApiConstants {
  static const String baseUrl = 'http://192.168.0.26:5000';
  static const String apiPath = '/api';
  
  // Endpoints
  static const String health = '$apiPath/health';
  static const String furniture = '$apiPath/furniture';
  static const String analyzeRoom = '$apiPath/analyze-room';
  static const String analyzeRoomTest = '$apiPath/analyze-room/test';
  
  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 60);
}
```

---

## API Service Layer

### Create HTTP Client

```dart
// lib/services/api_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../constants/api_constants.dart';

class ApiService {
  final http.Client _httpClient = http.Client();

  // GET request
  Future<dynamic> get(String endpoint) async {
    try {
      final response = await _httpClient
          .get(Uri.parse('${ApiConstants.baseUrl}$endpoint'))
          .timeout(ApiConstants.receiveTimeout);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Error: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('API Error: $e');
    }
  }

  // POST request with multipart (file upload)
  Future<dynamic> postFile(
    String endpoint,
    String fieldName,
    File file,
  ) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('${ApiConstants.baseUrl}$endpoint'),
      );

      request.files.add(
        await http.MultipartFile.fromPath(fieldName, file.path),
      );

      var response = await request.send().timeout(
            ApiConstants.receiveTimeout,
          );

      if (response.statusCode == 200) {
        var responseBody = await response.stream.bytesToString();
        return jsonDecode(responseBody);
      } else {
        throw Exception('Error: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('API Error: $e');
    }
  }
}
```

---

## Feature: Furniture Browse

### 1. Furniture Repository

```dart
// lib/repositories/furniture_repository.dart
import '../services/api_service.dart';
import '../models/furniture.dart';

class FurnitureRepository {
  final ApiService _apiService = ApiService();

  Future<List<Furniture>> getAllFurniture({
    String? category,
    String? style,
  }) async {
    String endpoint = ApiConstants.furniture;
    
    Map<String, String> params = {};
    if (category != null) params['category'] = category;
    if (style != null) params['style'] = style;

    if (params.isNotEmpty) {
      endpoint += '?' + params.entries
          .map((e) => '${e.key}=${e.value}')
          .join('&');
    }

    final data = await _apiService.get(endpoint);
    final furnitureList = (data['data'] as List)
        .map((item) => Furniture.fromJson(item))
        .toList();
    
    return furnitureList;
  }

  Future<Furniture> getFurnitureById(String id) async {
    final data = await _apiService.get('${ApiConstants.furniture}/$id');
    return Furniture.fromJson(data['data']);
  }

  Future<List<Furniture>> getFurnitureByIds(List<String> ids) async {
    final idsString = ids.join(',');
    final data = await _apiService
        .get('${ApiConstants.furniture}/ids?ids=$idsString');
    final furnitureList = (data['data'] as List)
        .map((item) => Furniture.fromJson(item))
        .toList();
    
    return furnitureList;
  }
}
```

### 2. Provider/State Management

```dart
// lib/providers/furniture_provider.dart
import 'package:flutter/material.dart';
import '../repositories/furniture_repository.dart';
import '../models/furniture.dart';

class FurnitureProvider extends ChangeNotifier {
  final FurnitureRepository _repository = FurnitureRepository();
  
  List<Furniture> _furniture = [];
  String? _selectedCategory;
  String? _selectedStyle;
  bool _isLoading = false;
  String? _error;

  List<Furniture> get furniture => _furniture;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> fetchFurniture({String? category, String? style}) async {
    _isLoading = true;
    _error = null;
    _selectedCategory = category;
    _selectedStyle = style;
    
    notifyListeners();

    try {
      _furniture = await _repository.getAllFurniture(
        category: category,
        style: style,
      );
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Furniture> getFurnitureDetail(String id) async {
    return await _repository.getFurnitureById(id);
  }
}
```

### 3. UI Widget

```dart
// lib/screens/furniture_list_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/furniture_provider.dart';

class FurnitureListScreen extends StatefulWidget {
  @override
  _FurnitureListScreenState createState() => _FurnitureListScreenState();
}

class _FurnitureListScreenState extends State<FurnitureListScreen> {
  @override
  void initState() {
    super.initState();
    context.read<FurnitureProvider>().fetchFurniture();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Furniture Catalog')),
      body: Consumer<FurnitureProvider>(
        builder: (context, provider, child) {
          if (provider.isLoading) {
            return Center(child: CircularProgressIndicator());
          }
          
          if (provider.error != null) {
            return Center(child: Text('Error: ${provider.error}'));
          }

          return GridView.builder(
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              childAspectRatio: 0.8,
            ),
            itemCount: provider.furniture.length,
            itemBuilder: (context, index) {
              final item = provider.furniture[index];
              return FurnitureCard(furniture: item);
            },
          );
        },
      ),
    );
  }
}

class FurnitureCard extends StatelessWidget {
  final Furniture furniture;
  
  const FurnitureCard({required this.furniture});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => FurnitureDetailScreen(
              furnitureId: furniture.id,
            ),
          ),
        );
      },
      child: Card(
        child: Column(
          children: [
            Image.network(
              '${ApiConstants.baseUrl}${furniture.thumbnailUrl}',
              height: 150,
              fit: BoxFit.cover,
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Column(
                children: [
                  Text(furniture.name, style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(furniture.category, style: TextStyle(fontSize: 12)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Feature: Room Analysis

### 1. Room Analysis Provider

```dart
// lib/providers/room_analysis_provider.dart
import 'package:flutter/material.dart';
import 'dart:io';
import '../repositories/furniture_repository.dart';
import '../models/room_analysis.dart';

class RoomAnalysisProvider extends ChangeNotifier {
  final FurnitureRepository _repository = FurnitureRepository();
  
  RoomAnalysis? _analysis;
  bool _isAnalyzing = false;
  String? _error;

  RoomAnalysis? get analysis => _analysis;
  bool get isAnalyzing => _isAnalyzing;
  String? get error => _error;

  Future<void> analyzeRoom(File imageFile) async {
    _isAnalyzing = true;
    _error = null;
    notifyListeners();

    try {
      final data = await _repository.analyzeRoom(imageFile);
      _analysis = RoomAnalysis.fromJson(data);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isAnalyzing = false;
      notifyListeners();
    }
  }

  void reset() {
    _analysis = null;
    _error = null;
    notifyListeners();
  }
}
```

### 2. Room Analysis UI

```dart
// lib/screens/room_analysis_screen.dart
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'dart:io';
import '../providers/room_analysis_provider.dart';

class RoomAnalysisScreen extends StatefulWidget {
  @override
  _RoomAnalysisScreenState createState() => _RoomAnalysisScreenState();
}

class _RoomAnalysisScreenState extends State<RoomAnalysisScreen> {
  File? _selectedImage;
  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.camera);
    
    if (pickedFile != null) {
      setState(() {
        _selectedImage = File(pickedFile.path);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Room Analysis')),
      body: Consumer<RoomAnalysisProvider>(
        builder: (context, provider, child) {
          if (provider.isAnalyzing) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Analyzing room...'),
                ],
              ),
            );
          }

          if (provider.analysis != null) {
            return RecommendationsView(analysis: provider.analysis!);
          }

          return Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (_selectedImage != null)
                Image.file(_selectedImage!, height: 300),
              SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: _pickImage,
                icon: Icon(Icons.camera),
                label: Text('Take Room Photo'),
              ),
              if (_selectedImage != null)
                ElevatedButton(
                  onPressed: () {
                    context.read<RoomAnalysisProvider>()
                        .analyzeRoom(_selectedImage!);
                  },
                  child: Text('Analyze Room'),
                ),
              if (provider.error != null)
                Padding(
                  padding: EdgeInsets.all(16),
                  child: Text('Error: ${provider.error}'),
                ),
            ],
          );
        },
      ),
    );
  }
}

class RecommendationsView extends StatelessWidget {
  final RoomAnalysis analysis;
  
  const RecommendationsView({required this.analysis});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: EdgeInsets.all(16),
      children: [
        Card(
          child: Padding(
            padding: EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Room Analysis',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                SizedBox(height: 10),
                Text('Room Type: ${analysis.analysis.roomType}'),
                Text('Style: ${analysis.analysis.style}'),
                Text('Colors: ${analysis.analysis.colors.join(", ")}'),
                Text('Lighting: ${analysis.analysis.lighting}'),
                SizedBox(height: 10),
                Text(
                  'Suggestions: ${analysis.analysis.suggestions}',
                  style: TextStyle(fontStyle: FontStyle.italic),
                ),
              ],
            ),
          ),
        ),
        SizedBox(height: 20),
        Text(
          'Recommended Furniture (${analysis.furniture.length})',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        ...analysis.furniture.map((furniture) {
          return Card(
            margin: EdgeInsets.only(top: 10),
            child: ListTile(
              leading: Image.network(
                '${ApiConstants.baseUrl}${furniture.thumbnailUrl}',
                width: 80,
                fit: BoxFit.cover,
              ),
              title: Text(furniture.name),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Score: ${furniture.recommendationScore}/100'),
                  Text('Style: ${furniture.style}'),
                ],
              ),
              trailing: Chip(
                label: Text('${furniture.recommendationScore}'),
              ),
            ),
          );
        }).toList(),
      ],
    );
  }
}
```

---

## Feature: Wishlist (Local Storage with Hive)

### 1. Wishlist Box Setup

```dart
// lib/main.dart
import 'package:hive_flutter/hive_flutter.dart';

void main() async {
  await Hive.initFlutter();
  runApp(MyApp());
}
```

### 2. Wishlist Provider

```dart
// lib/providers/wishlist_provider.dart
import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

class WishlistProvider extends ChangeNotifier {
  late Box<String> _wishlistBox;

  WishlistProvider() {
    _initializeBox();
  }

  Future<void> _initializeBox() async {
    _wishlistBox = await Hive.openBox<String>('wishlist');
  }

  List<String> get wishlist => _wishlistBox.values.toList();
  
  bool isInWishlist(String furnitureId) {
    return _wishlistBox.containsKey(furnitureId);
  }

  Future<void> addToWishlist(String furnitureId) async {
    await _wishlistBox.put(furnitureId, furnitureId);
    notifyListeners();
  }

  Future<void> removeFromWishlist(String furnitureId) async {
    await _wishlistBox.delete(furnitureId);
    notifyListeners();
  }

  Future<void> clearWishlist() async {
    await _wishlistBox.clear();
    notifyListeners();
  }
}
```

### 3. Wishlist Button Widget

```dart
// lib/widgets/wishlist_button.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/wishlist_provider.dart';

class WishlistButton extends StatelessWidget {
  final String furnitureId;

  const WishlistButton({required this.furnitureId});

  @override
  Widget build(BuildContext context) {
    return Consumer<WishlistProvider>(
      builder: (context, provider, child) {
        final isLiked = provider.isInWishlist(furnitureId);
        
        return IconButton(
          icon: Icon(
            isLiked ? Icons.favorite : Icons.favorite_border,
            color: isLiked ? Colors.red : Colors.grey,
          ),
          onPressed: () {
            if (isLiked) {
              provider.removeFromWishlist(furnitureId);
            } else {
              provider.addToWishlist(furnitureId);
            }
          },
        );
      },
    );
  }
}
```

---

## Network Configuration

### For Development (Laptop Access)

```dart
// Use local IP for both emulator and device testing
const String baseUrl = 'http://192.168.0.26:5000';
```

### For Production (Ngrok)

```dart
// Remove ngrok when deploying to production
const String baseUrl = 'https://your-production-domain.com';
```

### Test API Health

```dart
Future<void> testApiConnection() async {
  try {
    final response = await http.get(
      Uri.parse('$baseUrl/api/health'),
    ).timeout(Duration(seconds: 10));
    
    if (response.statusCode == 200) {
      print('✅ API Connected!');
    }
  } catch (e) {
    print('❌ API Error: $e');
  }
}
```

---

## Error Handling Best Practices

```dart
// lib/utils/error_handler.dart
class ErrorHandler {
  static String getErrorMessage(dynamic error) {
    if (error is SocketException) {
      return 'No internet connection';
    } else if (error is TimeoutException) {
      return 'Request timeout. Please try again.';
    } else if (error is HttpException) {
      return 'Server error. Please try again later.';
    } else {
      return error.toString();
    }
  }
}
```

---

## Performance Tips

1. **Use CachedNetworkImage** for thumbnails
2. **Pagination** for large furniture lists
3. **Lazy loading** for room analysis results
4. **Cache API responses** in local storage
5. **Compress images** before upload (max 10MB)
6. **Implement search** with debouncing

---

## Testing Checklist

- [ ] Test furniture list loading
- [ ] Test category/style filtering
- [ ] Test furniture detail page
- [ ] Test image picker for room analysis
- [ ] Test room analysis API (allow 60s timeout)
- [ ] Test wishlist add/remove
- [ ] Test 3D model loading
- [ ] Test with slow network (throttle in DevTools)
- [ ] Test offline mode gracefully
- [ ] Test error states

---

**Questions?** Contact the API team or check backend logs with:
```bash
docker logs gruhaalankar-app-1
```
