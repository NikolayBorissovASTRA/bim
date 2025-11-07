Option Explicit

' ================================================================================
' Simplified Shared Pyramids Validator
' ================================================================================
' Validates:
' 1. Each segment shares at least one pyramid with another segment
' 2. All pyramids in 'models' have coordinates in 'pyramid-coordinates'
'
' Usage: Press Alt+F8, select ValidateSharedPyramids, click Run
' ================================================================================

Sub ValidateSharedPyramids()
    Dim wsModels As Worksheet, wsCoords As Worksheet, wsReport As Worksheet
    Dim segments As Object, pyramidsWithCoords As Object, pyramidsInModels As Object
    Dim i As Long, j As Long, lastRow As Long, reportRow As Long
    Dim segment As String, pyramid As String

    ' Get worksheets
    On Error Resume Next
    Set wsModels = ThisWorkbook.Sheets("models")
    Set wsCoords = ThisWorkbook.Sheets("pyramid-coordinates")
    On Error GoTo 0

    If wsModels Is Nothing Or wsCoords Is Nothing Then
        MsgBox "Required sheets not found!" & vbCrLf & "Need: 'models' and 'pyramid-coordinates'", vbCritical
        Exit Sub
    End If

    ' Initialize data structures
    Set segments = CreateObject("Scripting.Dictionary")
    Set pyramidsWithCoords = CreateObject("Scripting.Dictionary")
    Set pyramidsInModels = CreateObject("Scripting.Dictionary")

    ' Read coordinates
    lastRow = wsCoords.Cells(wsCoords.Rows.Count, "A").End(xlUp).Row
    For i = 2 To lastRow
        pyramid = Trim(wsCoords.Cells(i, 1).Value)
        If pyramid <> "" Then pyramidsWithCoords(pyramid) = True
    Next i

    ' Read models and build segment groups
    lastRow = wsModels.Cells(wsModels.Rows.Count, "A").End(xlUp).Row
    For i = 2 To lastRow
        segment = Trim(wsModels.Cells(i, 1).Value)
        pyramid = Trim(wsModels.Cells(i, 2).Value)

        If segment <> "" And pyramid <> "" Then
            pyramidsInModels(pyramid) = True

            If Not segments.Exists(segment) Then
                Set segments(segment) = CreateObject("Scripting.Dictionary")
            End If
            segments(segment)(pyramid) = True
        End If
    Next i

    ' Create report sheet
    Application.DisplayAlerts = False
    On Error Resume Next: ThisWorkbook.Sheets("report").Delete: On Error GoTo 0
    Application.DisplayAlerts = True

    Set wsReport = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
    wsReport.Name = "report"

    ' Write headers
    With wsReport
        .Cells(1, 1).Value = "segment_1"
        .Cells(1, 2).Value = "segment_2"
        .Cells(1, 3).Value = "shared_pyramids"
        .Cells(1, 4).Value = "count"
        .Range("A1:D1").Font.Bold = True
        .Range("A1:D1").Interior.Color = RGB(200, 200, 200)
    End With

    reportRow = 2

    ' Find and report shared pyramids
    Dim segmentList As Variant, sharedList As String, sharedCount As Long
    Dim segmentHasSharing As Object, totalSharing As Long, totalSegments As Long
    Set segmentHasSharing = CreateObject("Scripting.Dictionary")

    segmentList = segments.Keys
    totalSegments = segments.Count

    For Each segment In segmentList
        segmentHasSharing(segment) = False
    Next segment

    ' Compare each segment pair
    For i = 0 To totalSegments - 1
        For j = i + 1 To totalSegments - 1
            Dim seg1 As String, seg2 As String
            seg1 = segmentList(i)
            seg2 = segmentList(j)

            ' Find shared pyramids
            sharedList = ""
            sharedCount = 0

            Dim pyr As Variant
            For Each pyr In segments(seg1).Keys
                If segments(seg2).Exists(pyr) Then
                    If sharedList <> "" Then sharedList = sharedList & ", "
                    sharedList = sharedList & pyr
                    sharedCount = sharedCount + 1
                End If
            Next pyr

            ' Write to report if shared pyramids found
            If sharedCount > 0 Then
                With wsReport
                    .Cells(reportRow, 1).Value = seg1
                    .Cells(reportRow, 2).Value = seg2
                    .Cells(reportRow, 3).Value = sharedList
                    .Cells(reportRow, 4).Value = sharedCount
                End With
                reportRow = reportRow + 1
                segmentHasSharing(seg1) = True
                segmentHasSharing(seg2) = True
            End If
        Next j
    Next i

    totalSharing = reportRow - 2

    ' Add isolated segments
    For Each segment In segmentList
        If Not segmentHasSharing(segment) Then
            With wsReport
                .Cells(reportRow, 1).Value = segment
                .Cells(reportRow, 2).Value = "NO SHARING"
                .Cells(reportRow, 3).Value = "This segment has no shared pyramids"
                .Cells(reportRow, 4).Value = 0
                .Range("A" & reportRow & ":D" & reportRow).Interior.Color = RGB(255, 200, 200)
            End With
            reportRow = reportRow + 1
        End If
    Next segment

    ' Add summary
    Dim segmentsWithSharing As Long
    segmentsWithSharing = 0
    For Each segment In segmentList
        If segmentHasSharing(segment) Then segmentsWithSharing = segmentsWithSharing + 1
    Next segment

    With wsReport
        .Cells(reportRow, 1).Value = "SUMMARY"
        .Cells(reportRow, 2).Value = totalSegments & " segments, " & segmentsWithSharing & " have sharing"
        .Cells(reportRow, 3).Value = totalSharing & " sharing pairs"
        .Range("A" & reportRow & ":D" & reportRow).Font.Bold = True
        .Range("A" & reportRow & ":D" & reportRow).Interior.Color = RGB(200, 220, 255)
    End With

    reportRow = reportRow + 2

    ' Check for missing coordinates
    Dim missingCoords As Collection, missingCount As Long
    Set missingCoords = New Collection

    For Each pyramid In pyramidsInModels.Keys
        If Not pyramidsWithCoords.Exists(pyramid) Then
            missingCoords.Add pyramid
        End If
    Next pyramid

    missingCount = missingCoords.Count

    ' Report missing coordinates
    If missingCount > 0 Then
        With wsReport
            .Cells(reportRow, 1).Value = "PYRAMIDS WITHOUT COORDINATES"
            .Range("A" & reportRow & ":D" & reportRow).Font.Bold = True
            .Range("A" & reportRow & ":D" & reportRow).Interior.Color = RGB(255, 200, 200)
            reportRow = reportRow + 1

            .Cells(reportRow, 1).Value = "pyramid_name"
            .Cells(reportRow, 2).Value = "status"
            .Cells(reportRow, 3).Value = "issue"
            .Range("A" & reportRow & ":D" & reportRow).Font.Bold = True
            .Range("A" & reportRow & ":D" & reportRow).Interior.Color = RGB(220, 220, 220)
            reportRow = reportRow + 1

            For Each pyramid In missingCoords
                .Cells(reportRow, 1).Value = pyramid
                .Cells(reportRow, 2).Value = "MISSING"
                .Cells(reportRow, 3).Value = "Referenced in 'models' but not in 'pyramid-coordinates'"
                .Range("A" & reportRow & ":D" & reportRow).Interior.Color = RGB(255, 220, 180)
                reportRow = reportRow + 1
            Next pyramid
        End With
    End If

    ' Auto-fit columns
    wsReport.Columns("A:D").AutoFit
    wsReport.Activate

    ' Validation result
    Dim allValid As Boolean
    allValid = (segmentsWithSharing = totalSegments) And (missingCount = 0)

    If allValid Then
        MsgBox "✓ PASSED" & vbCrLf & vbCrLf & _
               "All segments share pyramids" & vbCrLf & _
               "All pyramids have coordinates", vbInformation, "Validation Success"
    Else
        Dim msg As String
        msg = "✗ FAILED" & vbCrLf & vbCrLf

        If segmentsWithSharing < totalSegments Then
            msg = msg & "• " & (totalSegments - segmentsWithSharing) & " segment(s) without sharing" & vbCrLf
        End If

        If missingCount > 0 Then
            msg = msg & "• " & missingCount & " pyramid(s) missing coordinates" & vbCrLf
        End If

        msg = msg & vbCrLf & "See 'report' sheet for details"
        MsgBox msg, vbExclamation, "Validation Failed"
    End If
End Sub
