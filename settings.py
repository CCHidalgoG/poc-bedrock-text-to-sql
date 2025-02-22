DOMAIN_DESCRIPTIONS = {
    "fraude_bancos": {
        "schema": "fraud",
        "table": "bank_transaction_fraud_detection",
        "columns": {
            "Customer_ID": "Un identificador único para cada cliente dentro del sistema del banco.",
            "Customer_Name": "El nombre del cliente que realiza la transacción.",
            "Gender": "El género del cliente (por ejemplo, Masculino, Femenino, Otro).",
            "Age": "La edad del cliente en el momento de la transacción.",
            "State": "La nación donde reside el cliente.",
            "City": "La ciudad donde vive el cliente.",
            "Bank_Branch": "La sucursal bancaria específica donde el cliente tiene su cuenta.",
            "Account_Type": "El tipo de cuenta que tiene el cliente (por ejemplo, Ahorros, Corriente).",
            "Transaction_ID": "Un identificador único para cada transacción.",
            "Transaction_Date": "La fecha en la que ocurrió la transacción.",
            "Transaction_Time": "La hora específica en la que se inició la transacción.",
            "Transaction_Amount": "El valor financiero de la transacción.",
            "Merchant_ID": "Un identificador único para el comerciante involucrado en la transacción.",
            "Transaction_Type": "La naturaleza de la transacción (por ejemplo, Retiro, Depósito, Transferencia).",
            "Merchant_Category": "La categoría del comerciante (por ejemplo, Retail, Online, Viajes).",
            "Account_Balance": "El saldo de la cuenta del cliente después de la transacción.",
            "Transaction_Device": "La herramienta utilizada por el cliente para realizar la transacción (por ejemplo, Móvil, Escritorio).",
            "Transaction_Location": "La ubicación geográfica (por ejemplo, latitud, longitud) de la transacción.",
            "Device_Type": "El tipo de dispositivo utilizado para la transacción (por ejemplo, Smartphone, Laptop).",
            "Is_Fraud": "Un indicador binario (1 o 0) que indica si la transacción es fraudulenta o no.",
            "Transaction_Currency": "La moneda utilizada para la transacción (por ejemplo, USD, EUR).",
            "Customer_Contact": "El número de contacto del cliente.",
            "Transaction_Description": "Una breve descripción de la transacción (por ejemplo, compra, transferencia).",
            "Customer_Email": "La dirección de correo electrónico asociada a la cuenta del cliente."
        }
    }
}