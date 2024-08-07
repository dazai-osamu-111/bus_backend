import json
import uuid
import requests
import hmac
import hashlib

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class MomoView(APIView):
    permission_classes = [IsAuthenticated]
    # parameters send to MoMo get get payUrl
    def get(self, request):
        endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
        accessKey = "F8BBA842ECF85"
        secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
        orderInfo = "pay with MoMo"
        partnerCode = "MOMO"
        amount = request.query_params.get('amount')
        orderId = str(uuid.uuid4())
        requestId = orderId
        ipnUrl = "http://ducnt"
        redirectUrl = "example://momo_callback?orderId=" + orderId
        extraData = ""  # pass empty value or Encode base64 JsonString
        partnerName = "MoMo Payment"
        requestType = "captureWallet"
        storeId = "Test Store"
        orderGroupId = ""
        autoCapture = True
        lang = "vi"
        orderGroupId = ""
        system_order_id = orderId

        # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
        # &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
        # &requestType=$requestType
        rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId \
                       + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl \
                       + "&requestId=" + requestId + "&requestType=" + requestType

        # puts raw signature
        print("--------------------RAW SIGNATURE----------------")
        print(rawSignature)
        # signature
        h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
        signature = h.hexdigest()
        print("--------------------SIGNATURE----------------")
        print(signature)

        # json object send to MoMo endpoint

        data = {
            'partnerCode': partnerCode,
            'orderId': orderId,
            'partnerName': partnerName,
            'storeId': storeId,
            'ipnUrl': ipnUrl,
            'amount': amount,
            'lang': lang,
            'requestType': requestType,
            'redirectUrl': redirectUrl,
            'autoCapture': autoCapture,
            'orderInfo': orderInfo,
            'requestId': requestId,
            'extraData': extraData,
            'signature': signature,
            'orderGroupId': orderGroupId
        }

        print("--------------------JSON REQUEST----------------\n")
        data = json.dumps(data)
        print(data)

        clen = len(data)
        response = requests.post(endpoint, data=data,
                                 headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

        # f.close()
        print("--------------------JSON response----------------\n")
        print(response.json())

        return Response(response.json())

class MomoStatusView(APIView):
    def get(self, request):
        endpoint = "https://test-payment.momo.vn/v2/gateway/api/query"
        accessKey = "F8BBA842ECF85"
        secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
        partnerCode = "MOMO"
        orderId = request.query_params.get('orderId')
        requestId = orderId
        lang = "vi"

        # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl
        # &orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId
        # &requestType=$requestType
        rawSignature = "accessKey=" + accessKey + "&orderId=" + orderId \
                    + "&partnerCode=" + partnerCode  \
                       + "&requestId=" + requestId

        # puts raw signature
        print("--------------------RAW SIGNATURE----------------")
        print(rawSignature)
        # signature
        h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
        signature = h.hexdigest()
        print("--------------------SIGNATURE----------------")
        print(signature)

        # json object send to MoMo endpoint

        data = {
            'partnerCode': partnerCode,
            'orderId': orderId,
            'lang': lang,
            'requestId': requestId,
            'signature': signature,
        }

        print("--------------------JSON REQUEST----------------\n")
        data = json.dumps(data)
        print(data)

        clen = len(data)
        response = requests.post(endpoint, data=data,
                                 headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

        # f.close()
        print("--------------------JSON response----------------\n")
        print(response.json())
        return Response(response.json())
