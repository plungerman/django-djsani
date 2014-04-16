    created_at (
        DateTimeField
    )
    updated_at (
        DateTimeField
    )
    opt_out (
        boolean
        default=False
    )
    secondary (
        boolean
        default=False
    )

    primary_policy_holder (
        varchar 128
        required=False
    )
    primary_dob (
        date
        required=False
    )
    primary_company (
        varchar 128,
        required=False
    )
    primary_phone (
        varchar 12
        required=False
    )
    primary_member_id (
        varchar 64
        required=False
    )
    primary_group_no (
        varchar 64
        required=False
    )
    primary_policy_type (
        varchar 128
        required=False
    )
    primary_address (
        text
        required=False
    )

    secondary_policy_holder (
        varchar 128
        required=False
    )
    secondary_dob (
        date
        required=False
    )
    secondary_company (
        varchar 128,
        required=False
    )
    secondary_phone (
        varchar 12
        required=False
    )
    secondary_member_id (
        varchar 64
        required=False
    )
    secondary_group_no (
        varchar 64
        required=False
    )
    secondary_policy_type (
        varchar 128
        required=False
    )
    secondary_address (
        text
        required=False
    )
