
    created_at (
        DateTimeField
        auto_now_add=True
    )
    updated_at (
        DateTimeField
        auto_now=True
    )
    opt_out (
        required=False
        default=False
    )

    policy_holder (
        varchar 128
        required=False
    )
    dob (
        date
        required=False
    )
    company (
        varchar 128,
        required=False
    )
    phone (
        varchar 12
        required=False
    )
    member_id (
        varchar 64
        required=False
    )
    group_no (
        varchar 64
        required=False
    )
    policy_type (
        varchar 128
        required=False
    )
    address (
        text
        required=False
    )


