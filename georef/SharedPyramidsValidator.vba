Option Explicit

' ================================================================================
' Shared Pyramids Validator VBA Script
' ================================================================================
' This script validates that each segment_model shares at least one pyramid_name
' with another segment_model and generates a report in the 'report' sheet.
'
' Usage:
' 1. Open the Excel file with 'models' sheet
' 2. Press Alt+F11 to open VBA editor
' 3. Insert > Module
' 4. Paste this code
' 5. Run ValidateSharedPyramids macro (Alt+F8)
'
' Requirements:
' - Sheet 'models' with columns: segment_model, pyramid_name
' - Script will create/replace 'report' sheet
' ================================================================================

Sub ValidateSharedPyramids()
    Dim wsModels As Worksheet
    Dim wsReport As Worksheet
    Dim lastRow As Long
    Dim i As Long, j As Long
    Dim reportRow As Long

    ' Data structures
    Dim segments As Object  ' Dictionary of segments
    Dim segmentPyramids As Object  ' Dictionary: segment -> Collection of pyramids
    Dim segmentHasSharing As Object  ' Dictionary: segment -> Boolean
    Dim sharedPyramids As Object  ' Dictionary to track unique shared pyramids

    ' Variables for processing
    Dim segment1 As String, segment2 As String
    Dim pyramid As String
    Dim shared As Collection
    Dim sharedList As String
    Dim segmentList() As String
    Dim segmentCount As Long
    Dim totalSharedPyramids As Long
    Dim totalSharingPairs As Long
    Dim segmentsWithSharing As Long

    ' Initialize dictionaries
    Set segments = CreateObject("Scripting.Dictionary")
    Set segmentPyramids = CreateObject("Scripting.Dictionary")
    Set segmentHasSharing = CreateObject("Scripting.Dictionary")
    Set sharedPyramids = CreateObject("Scripting.Dictionary")

    ' Get models worksheet
    On Error Resume Next
    Set wsModels = ThisWorkbook.Sheets("models")
    On Error GoTo 0

    If wsModels Is Nothing Then
        MsgBox "Sheet 'models' not found!", vbCritical
        Exit Sub
    End If

    ' Clear/create report sheet
    On Error Resume Next
    Application.DisplayAlerts = False
    ThisWorkbook.Sheets("report").Delete
    Application.DisplayAlerts = True
    On Error GoTo 0

    Set wsReport = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
    wsReport.Name = "report"

    ' Write report headers
    wsReport.Cells(1, 1).Value = "segment_1"
    wsReport.Cells(1, 2).Value = "segment_2"
    wsReport.Cells(1, 3).Value = "shared_pyramids"
    wsReport.Cells(1, 4).Value = "count"

    ' Format headers
    With wsReport.Range("A1:D1")
        .Font.Bold = True
        .Interior.Color = RGB(200, 200, 200)
    End With

    reportRow = 2

    ' Read data from models sheet
    lastRow = wsModels.Cells(wsModels.Rows.Count, "A").End(xlUp).Row

    ' Build segment -> pyramids mapping
    For i = 2 To lastRow  ' Assuming row 1 is header
        segment1 = Trim(wsModels.Cells(i, 1).Value)  ' segment_model column
        pyramid = Trim(wsModels.Cells(i, 2).Value)   ' pyramid_name column

        If segment1 <> "" And pyramid <> "" Then
            ' Add segment to list
            If Not segments.Exists(segment1) Then
                segments.Add segment1, True
                Set segmentPyramids(segment1) = CreateObject("Scripting.Dictionary")
                segmentHasSharing.Add segment1, False
            End If

            ' Add pyramid to segment
            If Not segmentPyramids(segment1).Exists(pyramid) Then
                segmentPyramids(segment1).Add pyramid, True
            End If
        End If
    Next i

    ' Convert segments dictionary to array
    segmentList = segments.Keys
    segmentCount = segments.Count

    ' Find shared pyramids between segment pairs
    For i = 0 To segmentCount - 1
        segment1 = segmentList(i)

        For j = i + 1 To segmentCount - 1
            segment2 = segmentList(j)

            ' Find intersection of pyramids
            Set shared = New Collection
            sharedList = ""

            Dim pyramid1 As Variant
            For Each pyramid1 In segmentPyramids(segment1).Keys
                If segmentPyramids(segment2).Exists(pyramid1) Then
                    shared.Add pyramid1
                    If sharedList = "" Then
                        sharedList = pyramid1
                    Else
                        sharedList = sharedList & ", " & pyramid1
                    End If
                End If
            Next pyramid1

            ' If there are shared pyramids, write to report
            If shared.Count > 0 Then
                wsReport.Cells(reportRow, 1).Value = segment1
                wsReport.Cells(reportRow, 2).Value = segment2
                wsReport.Cells(reportRow, 3).Value = sharedList
                wsReport.Cells(reportRow, 4).Value = shared.Count

                ' Mark both segments as having sharing
                segmentHasSharing(segment1) = True
                segmentHasSharing(segment2) = True

                ' Track unique shared pyramids
                Dim p As Variant
                For Each p In shared
                    If Not sharedPyramids.Exists(p) Then
                        sharedPyramids.Add p, True
                    End If
                Next p

                reportRow = reportRow + 1
            End If
        Next j
    Next i

    totalSharingPairs = reportRow - 2

    ' Add rows for isolated segments (segments without sharing)
    For i = 0 To segmentCount - 1
        segment1 = segmentList(i)
        If Not segmentHasSharing(segment1) Then
            wsReport.Cells(reportRow, 1).Value = segment1
            wsReport.Cells(reportRow, 2).Value = "NO SHARING"
            wsReport.Cells(reportRow, 3).Value = "This segment has no shared pyramids with any other segment"
            wsReport.Cells(reportRow, 4).Value = 0

            ' Highlight isolated segment row in red
            With wsReport.Range("A" & reportRow & ":D" & reportRow)
                .Interior.Color = RGB(255, 200, 200)
            End With

            reportRow = reportRow + 1
        End If
    Next i

    ' Count segments with sharing
    segmentsWithSharing = 0
    For i = 0 To segmentCount - 1
        If segmentHasSharing(segmentList(i)) Then
            segmentsWithSharing = segmentsWithSharing + 1
        End If
    Next i

    ' Add summary row
    totalSharedPyramids = sharedPyramids.Count

    wsReport.Cells(reportRow, 1).Value = "SUMMARY"
    wsReport.Cells(reportRow, 2).Value = segmentCount & " segments total, " & segmentsWithSharing & " have sharing"
    wsReport.Cells(reportRow, 3).Value = totalSharedPyramids & " unique pyramids are shared across " & totalSharingPairs & " segment pairs"
    wsReport.Cells(reportRow, 4).Value = totalSharedPyramids

    ' Format summary row
    With wsReport.Range("A" & reportRow & ":D" & reportRow)
        .Font.Bold = True
        .Interior.Color = RGB(200, 220, 255)
    End With

    ' Auto-fit columns
    wsReport.Columns("A:D").AutoFit

    ' Validation result
    Dim allValid As Boolean
    allValid = (segmentsWithSharing = segmentCount)

    If allValid Then
        MsgBox "✓ PASSED: Each segment has at least one shared pyramid!" & vbCrLf & vbCrLf & _
               "Report written to 'report' sheet", vbInformation, "Validation Successful"
    Else
        Dim missingCount As Long
        missingCount = segmentCount - segmentsWithSharing
        MsgBox "✗ FAILED: " & missingCount & " segment(s) have no shared pyramids!" & vbCrLf & vbCrLf & _
               "See 'report' sheet for details (isolated segments highlighted in red)", vbExclamation, "Validation Failed"
    End If

    ' Activate report sheet
    wsReport.Activate
End Sub

' ================================================================================
' Helper Function: Check if Collection Contains Item
' ================================================================================
Function CollectionContains(col As Collection, item As Variant) As Boolean
    Dim obj As Variant
    For Each obj In col
        If obj = item Then
            CollectionContains = True
            Exit Function
        End If
    Next obj
    CollectionContains = False
End Function
