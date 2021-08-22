# FaceServer

## Set-up

```
# sudo ./nvinstall.sh
# sudo ./install.sh
```

## Usage

```
# python3 main.py config/client.conf
```

## Configurations

<table>
  <tr>
    <td colspan=2 align=center><b>graphical</b></td>
  </tr>
  <tr>
    <td>enabled</td>
    <td>Enable GUI or not (not used).</td>
  </tr>
  <tr>
    <td colspan=2 align=center><b>listener</b></td>
  </tr>
  <tr>
    <td>enabled</td>
    <td>Enable listener or not.</td>
  </tr>
  <tr>
    <td>listener_addr</td>
    <td>Listening address of listener.</td>
  </tr>
  <tr>
    <td>listener_port</td>
    <td>Listening port of listener.</td>
  </tr>
  <tr>
    <td colspan=2 align=center><b>reporter</b></td>
  </tr>
  <tr>
    <td>enabled</td>
    <td>Enable reporter or not.</td>
  </tr>
  <tr>
    <td>collector_addr</td>
    <td>Address of remote collector</td>
  </tr>
  <tr>
    <td>collector_port</td>
    <td>Port of remote collector</td>
  </tr>
  <tr>
    <td>collect_info_period</td>
    <td>Period of collecting system-level and process-level information.</td>
  </tr>
  <tr>
    <td>send_report_period</td>
    <td>Period of sending report to collector</td>
  </tr>
</table>

## Handlers

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>0</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>TxHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Transmit data through network</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>data to be transmit</td>
  </tr>
  <tr>
    <td rowspan=3><b>parameters</b></td>
    <td>addr</td>
    <td>Target address</td>
  </tr>
  <tr>
    <td>port</td>
    <td>Target port</td>
  </tr>
  <tr>
    <td>protocol</td>
    <td>Via TCP / UDP</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>1</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>RxHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Receive data from network</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Received data.</td>
  </tr>
  <tr>
    <td rowspan=3><b>parameters</b></td>
    <td>addr</td>
    <td>Listening address</td>
  </tr>
  <tr>
    <td>port</td>
    <td>Listening port</td>
  </tr>
  <tr>
    <td>protocol</td>
    <td>Via TCP / UDP</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>2</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>CaptureHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Capture images from camera.</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>captured images.</td>
  </tr>
  <tr>
    <td rowspan=4><b>parameters</b></td>
    <td>source</td>
    <td>Value 0 indicating the default building camera.</td>
  </tr>
  <tr>
    <td>width</td>
    <td>Captured image width.</td>
  </tr>
  <tr>
    <td>height</td>
    <td>Captured image height.</td>
  </tr>
  <tr>
    <td>fps</td>
    <td>Frame rate of capturing images.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>3</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>RenderHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Render images to a window.</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Images to be rendered.</td>
  </tr>
  <tr>
    <td width=110><b>parameters</b></td>
    <td>fps</td>
    <td>Frame rate of rendering images.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>4</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>ResizeHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>To resize images.</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Images to be resized.</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Resized images.</td>
  </tr>
  <tr>
    <td rowspan=2><b>parameters</b></td>
    <td>width</td>
    <td>Target width.</td>
  </tr>
  <tr>
    <td>height</td>
    <td>Target height.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>5</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>EncodeHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Encode images to JPEG format</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Images to be encoded.</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Encoded images.</td>
  </tr>
  <tr>
    <td width=110><b>parameters</b></td>
    <td>quality</td>
    <td>Compression quality of JPEG.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>6</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>DecodeHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Decode compressed images</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Images to be decoded.</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Decoded images.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>7</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>YoloDetectObjectHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Detect object from images</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Images</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Locations of detected objects and their cropped images.</td>
  </tr>
  <tr>
    <td rowspan=5><b>parameters</b></td>
    <td>gpu</td>
    <td>Enable GPU utilization or not.</td>
  </tr>
  <tr>
    <td>config</td>
    <td>Model configurations.</td>
  </tr>
  <tr>
    <td>weights</td>
    <td>Model weights.</td>
  </tr>
  <tr>
    <td>labels</td>
    <td>Label of detected objects.</td>
  </tr>
  <tr>
    <td>targets</td>
    <td>Interested objects.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>8</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>HaarDetectFaceHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Detect faces with Haar feature-based detector</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>images</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Locations of detected faces and their cropped images.</td>
  </tr>
  <tr>
    <td rowspan=2><b>parameters</b></td>
    <td>scale_factor</td>
    <td>Upsample scale of detection (the larger the faster, but less accurate).</td>
  </tr>
  <tr>
    <td>min_size</td>
    <td>Minimum detect size.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>9</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>HogDetectFaceHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Detect faces with HoG-based detector</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Images</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Locations of detected faces and their cropped images.</td>
  </tr>
  <tr>
    <td width=110><b>parameters</b></td>
    <td>upsample</td>
    <td>Upsample times of detection (the larger the faster, but less accurate).</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>10</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>MmodDetectFaceHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Detect faces with depp learning-based MMOD Model</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Images</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Locations of detected faces and their cropped images.</td>
  </tr>
  <tr>
    <td rowspan=3><b>parameters</b></td>
    <td>model</td>
    <td>Model for detection</td>
  </tr>
  <tr>
    <td>upsample</td>
    <td>Upsample times of detection (the larger the faster, but less accurate).</td>
  </tr>
  <tr>
    <td>tresh</td>
    <td>Threshold of identifying faces.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>11</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>DlibAlignHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Align detected faces.</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Cropped faces.</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Aligned result</td>
  </tr>
  <tr>
    <td rowspan=3><b>parameters</b></td>
    <td>predictor</td>
    <td>Model for alignment.</td>
  </tr>
  <tr>
    <td>indices</td>
    <td>Features for alignment.</td>
  </tr>
  <tr>
    <td>dim</td>
    <td>Resize size for alignment.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>12</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>MtcnnDetectFaceAlignHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Detect and align faces in an image</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>images</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Location and crop of detected and aligned faces</td>
  </tr>
  <tr>
    <td rowspan=3><b>parameters</b></td>
    <td>model</td>
    <td>Model for Detection.</td>
  </tr>
  <tr>
    <td>dim</td>
    <td>Dimension of model (network size).</td>
  </tr>
  <tr>
    <td>margin</td>
    <td>Padding of detected faces.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>13</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>DlibAlignRecognizeHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Align and recognize detected faces with Dlib model.</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Cropped faces</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Recongnized result (position & label)</td>
  </tr>
  <tr>
    <td rowspan=6> <b>parameters</b></td>
    <td>predictor</td>
    <td>Aligner.</td>
  </tr>
  <tr>
    <td>model</td>
    <td>Model for recognition.</td>
  </tr>
  <tr>
    <td>classifier</td>
    <td>Pretriained SVM classifier.</td>
  </tr>
  <tr>
    <td>dim</td>
    <td>Dimenssion of model (network size).</td>
  </tr>
  <tr>
    <td>jitters</td>
    <td>The larger the slower but more accurate.</td>
  </tr>
  <tr>
    <td>tresh</td>
    <td>Threshold of recognition.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>14</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>OpenfaceRecognizeHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Recognize faces with OpenFace model.</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Cropped faces</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Recognized result (position & label)</td>
  </tr>
  <tr>
    <td rowspan=4><b>parameters</b></td>
    <td>model</td>
    <td>Model for recognition.</td>
  </tr>
  <tr>
    <td>classifier</td>
    <td>Pre-trained SVM classifier <a
        href="https://cmusatyalab.github.io/openface/demo-3-classifier/">link here</a>.</td>
  </tr>
  <tr>
    <td>dim</td>
    <td>Dimension of model (network size).</td>
  </tr>
  <tr>
    <td>tresh</td>
    <td>Threshold of recognition.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>15</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>FacenetRecognizeHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Recognize faces with FaceNet model.</td>
  </tr>
  <tr>
    <td width=110><b>inputs</b></td>
    <td>0</td>
    <td>Cropped faces</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Recongnized result (position & label)</td>
  </tr>
  <tr>
    <td rowspan=4><b>parameters</b></td>
    <td>model</td>
    <td>Model for recognition.</td>
  </tr>
  <tr>
    <td>classifier</td>
    <td>Pretriained SVM classifier <a
        href="https://github.com/dav<b>ID</b>sandberg/facenet/wiki/Classifier-training-of-inception-resnet-v1">link
        here</a>.</td>
  </tr>
  <tr>
    <td>dim</td>
    <td>Dimension of model (network size).</td>
  </tr>
  <tr>
    <td>tresh</td>
    <td>Threshold of recognition.</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>16</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>DrawBoxesHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Draw boxes on image</td>
  </tr>
  <tr>
    <td rowspan=2><b>inputs</b></td>
    <td>0</td>
    <td>Images.</td>
  </tr>
  <tr>
    <td>1</td>
    <td>Locations of boxes.</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Drawn images</td>
  </tr>
</table>

<table>
  <tr>
    <td colspan=2 width=230><b>ID</b></td>
    <td width=450>17</td>
  </tr>
  <tr>
    <td colspan=2><b>name</b></td>
    <td>DrawLabeledBoxesHandler</td>
  </tr>
  <tr>
    <td colspan=2><b>description</b></td>
    <td>Draw boxes and labels on image</td>
  </tr>
  <tr>
    <td rowspan=2><b>inputs</b></td>
    <td>0</td>
    <td>Images.</td>
  </tr>
  <tr>
    <td>1</td>
    <td>Locations of boxes with labels.</td>
  </tr>
  <tr>
    <td width=110><b>outputs</b></td>
    <td>0</td>
    <td>Drawn images</td>
  </tr>
</table>
