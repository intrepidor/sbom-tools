' Visual Basic for Applications template

Sub HelloWorld()
    ' This macro displays a message box with "Hello, World!"
    MsgBox "Hello, World!"
End Sub

Sub Auto_Open()
    ' This macro runs when the workbook is opened
    MsgBox "Welcome to Excel VBA!"
End Sub

Sub Auto_Close()
    ' This macro runs when the workbook is closed
    MsgBox "Goodbye from Excel VBA!"
End Sub

' Function: Factorize
' Description: This function takes a long integer as input and returns an array of its prime factors.
' Parameters:
'   ByVal number As Long - The number to be factorized.
' Returns:
'   Variant - An array of long integers representing the prime factors of the input number.
' Example:
'   Dim factors() As Variant
'   factors = Factorize(60)
'   ' factors will contain [2, 2, 3, 5]
Function Factorize(ByVal number As Long) As Variant
    Dim factors() As Long
    ReDim factors(0)
    Dim i As Long
    For i = 2 To number
        If number Mod i = 0 Then
            factors(UBound(factors)) = i
            ReDim Preserve factors(UBound(factors) + 1)
            number = number / i
            i = 1
        End If
    Next i
    ReDim Preserve factors(UBound(factors) - 1)
    Factorize = factors
End Function

' Function: FindRowValue
' Description: This function searches for a specified value in the first column of a given range and returns the value
' in the last column of the same row where the specified value is found.
' Parameters:
'   - data (Range): The range of cells to search within.
'   - value (Variant): The value to search for in the first column of the range.
' Returns:
'   - Variant: The value in the last column of the row where the specified value is found. If the value is not found, it returns a #N/A error.
Function FindRowValue(ByVal data As Range, ByVal value As Variant) As Variant
    Dim i As Long
    For i = 1 To data.Rows.Count
        If data.Cells(i, 1).Value = value Then
            FindRowValue = data.Cells(i, data.Columns.Count).Value
            Exit Function
        End If
    Next i
    FindRowValue = CVErr(xlErrNA)
End Function

