def shared_info(page_name):

    page_name = page_name.split("/")[-1].replace(".py", "")

    pages = [
        {
            "short_name": "step1",
            "title": "Verify Hardware Configuration",
        },
        {
            "short_name": "board_input",
            "title": "Board Information",
        },
        {
            "short_name": "tests",
            "title": "Run Tests",
        },
        {
            "short_name": "test_report",
            "title": "Test Report",
        },
        {
            "short_name": "upload",
            "title": "Upload Report",
        },
    ]

    # Add options
    for i, page in enumerate(pages):
        page["options"] = []
        page["value"] = []
        for j, p in enumerate(pages):
            if j <= i:
                page["value"].append(p["short_name"])
            page["options"].append(
                {
                    "label": p["title"],
                    "value": p["short_name"],
                    "disabled": True,
                }
            )

    # add_progress_values
    num_pages = len(pages)
    for i, page in enumerate(pages):
        page["progress"] = 100 / num_pages * (i + 1)

    # Add next and previous page
    for i, page in enumerate(pages):
        if i == 0:
            page["prev"] = None
        else:
            page["prev"] = "/" + pages[i - 1]["short_name"].replace("_", "-")

        if i == num_pages - 1:
            page["next"] = None
        else:
            page["next"] = "/" + pages[i + 1]["short_name"].replace("_", "-")

    for page in pages:
        if page["short_name"] == page_name:
            print(page)
            return page

    raise ValueError(f"Page {page_name} not found in pages list")
