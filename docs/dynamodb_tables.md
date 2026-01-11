# DynamoDB Tables

## Books
- Partition Key: BookID (String)
- Attributes: Title, Author, TotalCopies, AvailableCopies

## Members
- Partition Key: MemberID (String)
- Attributes: Name, Email

## IssueRecords
- Partition Key: IssueID (String)
- Attributes: BookID, MemberID, IssueDate, ReturnDate
