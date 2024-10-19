import 'dart:convert';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class WelcomePage extends StatefulWidget {
  const WelcomePage({Key? key}) : super(key: key);

  @override
  State<WelcomePage> createState() => _WelcomePageState();
}

class _WelcomePageState extends State<WelcomePage> {
  final TextEditingController _sentence1Controller = TextEditingController();
  final TextEditingController _sentence2Controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage('lib/assets/background.png'),
            fit: BoxFit.cover,
          ),
        ),
        child: Stack(
          children: <Widget>[
            Center(
              child: Stack(
                children: [
                  Container(
                    padding: const EdgeInsets.all(20.0),
                    width: 600,
                    height: 300,
                    decoration: BoxDecoration(
                      color: const Color.fromARGB(255, 255, 255, 255)
                          .withOpacity(0.5),
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                  Positioned(
                    width: 600,
                    height: 300,
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: BackdropFilter(
                        filter: ImageFilter.blur(sigmaX: 20.0, sigmaY: 10.0),
                        child: Container(
                          width: 600,
                          height: 300,
                          decoration: BoxDecoration(
                            color: Colors.black.withOpacity(0.4), // 透明度较低的遮罩颜色
                          ),
                        ),
                      ),
                    ),
                  ),

                  // Positioned.fill(
                  //   child: BackdropFilter(
                  //     filter: ImageFilter.blur(sigmaX: 10.0, sigmaY: 10.0),
                  //     child: Container(
                  //       decoration: BoxDecoration(
                  //         color: Colors.black.withOpacity(0.5), // 透明颜色让毛玻璃效果可见
                  //         borderRadius: BorderRadius.circular(10),
                  //       ),
                  //     ),
                  //   ),
                  // ),
                  Container(
                    padding: const EdgeInsets.all(20.0),
                    width: 600,
                    height: 300,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        ConstrainedBox(
                          constraints: const BoxConstraints(
                            minWidth: double.infinity,
                            minHeight: 48,
                          ),
                          child: TextFormField(
                            controller: _sentence1Controller,
                            decoration: const InputDecoration(
                              filled: true,
                              fillColor: Colors.white,
                              border: OutlineInputBorder(
                                borderRadius:
                                    BorderRadius.all(Radius.circular(5)),
                                borderSide: BorderSide.none,
                              ),
                              enabledBorder: OutlineInputBorder(
                                borderSide: BorderSide.none,
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide: BorderSide.none,
                              ),
                              hintText: 'Sentence1',
                              hintStyle: TextStyle(color: Colors.grey),
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        ConstrainedBox(
                          constraints: const BoxConstraints(
                            minWidth: double.infinity,
                            minHeight: 48,
                          ),
                          child: TextFormField(
                            controller: _sentence2Controller,
                            decoration: const InputDecoration(
                              filled: true,
                              fillColor: Colors.white,
                              border: OutlineInputBorder(
                                borderRadius:
                                    BorderRadius.all(Radius.circular(5)),
                                borderSide: BorderSide.none,
                              ),
                              enabledBorder: OutlineInputBorder(
                                borderSide: BorderSide.none,
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide: BorderSide.none,
                              ),
                              hintText: 'Sentence2',
                              hintStyle: TextStyle(color: Colors.grey),
                            ),
                          ),
                        ),
                        const SizedBox(height: 40),
                        ConstrainedBox(
                          constraints: const BoxConstraints(
                            minWidth: double.infinity,
                            minHeight: 48,
                          ),
                          child: ElevatedButton(
                            onPressed: () {
                              _sendDataToBackend(_sentence1Controller.text,
                                  _sentence2Controller.text);
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor:
                                  const Color.fromARGB(255, 220, 235, 236),
                              foregroundColor:
                                  const Color.fromARGB(255, 185, 127, 222),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(10),
                              ),
                            ),
                            child: const Text('确认'),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _sendDataToBackend(String sentence1, String sentence2) async {
    var url = Uri.parse('http://wao.emorepitg.top:37101/predict');
    var response = await http.post(url,
        body: json.encode({
          'sentence1': sentence1,
          'sentence2': sentence2,
        }),
        headers: {'Content-Type': 'application/json'});

    if (response.statusCode == 200) {
      var prediction = json.decode(response.body)['prediction']; // 注意字段名
      Future.delayed(Duration.zero, () {
        _showResponseDialog(context, prediction ?? 'No prediction found');
      });
    } else {
      Future.delayed(Duration.zero, () {
        _showResponseDialog(context, 'Failed to get prediction');
      });
    }
  }

  void _showResponseDialog(BuildContext context, String response) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Prediction Result'),
          content: Text(response),
          actions: <Widget>[
            TextButton(
              child: const Text('Close'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }
}
