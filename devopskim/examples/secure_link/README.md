### **NGINX Secure Link 구성과 MD5 생성 스크립트를 통한 보안 링크 생성 및 검증 과정**

NGINX의 `ngx_http_secure_link_module`을 사용하여 요청의 무결성을 검증하고 링크 유효성을 관리합니다. 이를 통해 비인가 접근을 차단하고, 만료 시간을 설정하여 링크의 보안을 강화합니다. 아래는 주어진 설정과 스크립트를 기반으로 보안 링크 생성 및 검증 과정을 단계별로 설명한 내용입니다.

---

## **1. NGINX Secure Link 구성 분석**

### **구성 요소**
```nginx
location /download {
    secure_link $arg_md5,$arg_expires;
    secure_link_md5 "$uri$secure_link_expires secret";

    if ($secure_link = "") {
        return 403;
    }

    if ($secure_link = "0") {
        return 410;
    }

    internal_redirect @success;
}
```

1. **`secure_link` 디렉티브**:
   - `$arg_md5`: 요청에 포함된 `md5` 매개변수를 통해 해시값을 전달받음.
   - `$arg_expires`: 요청에 포함된 `expires` 매개변수를 통해 링크 만료 시간을 전달받음.

2. **`secure_link_md5` 디렉티브**:
   - `$uri`, `$secure_link_expires` (만료 시간) 및 `secret` 문자열을 조합하여 MD5 해시를 계산.

3. **검증 조건**:
   - `$secure_link` 값이 빈 문자열이면 (MD5 해시 불일치) HTTP 403 반환.
   - `$secure_link` 값이 `0`이면 (링크 만료) HTTP 410 반환.

4. **인증 성공 시 처리**:
   - 내부적으로 `@success`로 리다이렉트.

---

## **2. MD5 생성 스크립트 분석**
```bash
#!/bin/bash
echo -n '/download2147483647 secret' | \
    openssl md5 -binary | openssl base64 | tr +/ -_ | tr -d =
```

### **스크립트 역할**
1. **입력값 준비**:
   - `/download`: 요청 URI.
   - `2147483647`: 링크 만료 시간 (Unix Epoch 기준).
   - `secret`: 고정된 비밀 문자열.

2. **MD5 해시 계산**:
   - MD5 해시를 바이너리 형식으로 생성.

3. **Base64 URL-safe 인코딩**:
   - MD5 결과를 Base64로 인코딩.
   - `+`를 `-`로, `/`를 `_`로 변환하여 URL-safe 문자열로 변경.
   - 마지막 `=` 패딩 제거.

### **출력값**
- MD5 해시 값이 Base64 URL-safe 형식으로 출력됩니다. 이 값이 보안 링크의 `md5` 매개변수로 사용됩니다.

---

## **3. 보안 링크 생성 및 요청**

### **링크 생성**
1. URI: `/download`.
2. 만료 시간: `2147483647` (2038년 1월 19일 03:14:07 UTC).
3. MD5 해시: 스크립트 실행 결과값(예: `_e4Nc3iduzkWRm01TBBNYw`).

결과 링크:
```
/download?md5=_e4Nc3iduzkWRm01TBBNYw&expires=2147483647
```

---

## **4. 보안 링크 검증 과정**

### **NGINX 검증 로직**
1. **링크에 포함된 값 추출**:
   - 요청: `/download?md5=_e4Nc3iduzkWRm01TBBNYw&expires=2147483647`.
   - `$arg_md5`: `_e4Nc3iduzkWRm01TBBNYw`.
   - `$arg_expires`: `2147483647`.

2. **MD5 해시 재계산**:
   - `secure_link_md5`에서 설정한 표현식으로 해시 계산:
     ```bash
     echo -n '/download2147483647 secret' | openssl md5 -binary | openssl base64 | tr +/ -_ | tr -d =
     ```

3. **해시 비교**:
   - 요청에서 전달받은 `$arg_md5`와 계산된 MD5 해시값을 비교.
   - 일치하지 않으면 `$secure_link = ""`, HTTP 403 반환.

4. **링크 만료 시간 확인**:
   - 현재 시간이 `$arg_expires`보다 크면 `$secure_link = "0"`, HTTP 410 반환.

5. **인증 성공**:
   - 해시가 일치하고, 만료되지 않은 경우 `$secure_link = "1"`.
   - `internal_redirect @success`로 성공 처리.

---

## **5. 동작 시나리오**

### **유효한 링크 요청**
- 요청: `/download?md5=_e4Nc3iduzkWRm01TBBNYw&expires=2147483647`.
- 현재 시간: `2024년`.
- 결과:
  - MD5 해시 검증 통과.
  - 만료 시간 검증 통과.
  - 내부 리다이렉트 `@success`.

### **만료된 링크 요청**
- 요청: `/download?md5=_e4Nc3iduzkWRm01TBBNYw&expires=1609459200` (2021년 1월 1일).
- 현재 시간: `2024년`.
- 결과:
  - MD5 해시 검증 통과.
  - 만료 시간 초과 → HTTP 410 반환.

### **잘못된 해시 요청**
- 요청: `/download?md5=invalidhash&expires=2147483647`.
- 결과:
  - MD5 해시 불일치 → HTTP 403 반환.

---

## **결론**

이 구성은 다음과 같은 보안 기능을 제공합니다:
1. **무결성 검증**: 요청된 URI와 `secret`으로 생성한 해시값을 비교하여 변경 여부를 확인.
2. **만료 시간 설정**: 링크가 설정된 시간 이후에는 무효화.
3. **유연한 구성**: URI, 만료 시간, 비밀 문자열 조합으로 다양한 보안 시나리오에 대응 가능. 

이와 같은 설정은 파일 다운로드, API 보호 등 다양한 보안 시나리오에서 사용할 수 있습니다.