"""
Content for the synthetic policy documents.

Two fictional insurers, Northgate Insurance and Harbourline Insurance, with
deliberately different limits and excesses so the RAG system has to cite
the right document. All wording is original and fictional.

Block types used inside each section:
    ("p", text)                       a paragraph
    ("clause", number, title, text)   a numbered clause
    ("bullets", [items])              a bullet list
    ("table", [header, row, row...])  a table
"""

NORTHGATE = "Northgate Insurance"
HARBOURLINE = "Harbourline Insurance"

# ---------------------------------------------------------------------------
# 1. Northgate Home - IPID (short product summary)
# ---------------------------------------------------------------------------
NORTHGATE_HOME_IPID = {
    "doc_id": "northgate_home_ipid",
    "filename": "northgate_home_ipid.pdf",
    "insurer": NORTHGATE,
    "product": "Home",
    "doc_type": "IPID",
    "title": "Home Insurance - Insurance Product Information Document",
    "reference": "NG-HOME-IPID-2026",
    "effective_date": "1 January 2026",
    "intro": (
        "This document is a summary of the main features of Northgate Home Insurance. "
        "It does not contain the full terms and conditions. Full details are in the "
        "Northgate Home Insurance Policy Wording and your schedule."
    ),
    "sections": [
        {"number": "1", "heading": "What is this type of insurance?", "blocks": [
            ("p", "Northgate Home Insurance covers the structure of your home (buildings) and "
                  "your household goods and personal possessions (contents) against loss or "
                  "damage caused by events such as fire, storm, flood, theft and escape of water. "
                  "Your schedule shows whether you have buildings cover, contents cover, or both."),
        ]},
        {"number": "2", "heading": "What is insured?", "blocks": [
            ("bullets", [
                "Buildings up to the sum insured shown in your schedule.",
                "Contents up to the sum insured shown in your schedule.",
                "Alternative accommodation if your home cannot be lived in, up to 20% of the buildings sum insured.",
                "Trace and access to find the source of an escape of water, up to £5,000.",
                "Valuables up to £2,000 for any single item, unless specified on your schedule.",
                "Cash up to £500.",
                "Contents temporarily in the garden up to £1,000.",
            ]),
        ]},
        {"number": "3", "heading": "What is not insured?", "blocks": [
            ("bullets", [
                "The excess shown in section 4 of this document.",
                "Wear and tear or gradual deterioration.",
                "Damage caused by insects, vermin or pets.",
                "Loss or damage while your home is unoccupied for more than 60 consecutive days, for theft, escape of water and malicious damage.",
                "Accidental damage, unless you have chosen this optional cover.",
            ]),
        ]},
        {"number": "4", "heading": "Are there any restrictions on cover?", "blocks": [
            ("bullets", [
                "Standard excess of £250 applies to each claim.",
                "Escape of water excess of £500.",
                "Subsidence, heave and landslip excess of £1,000.",
                "Total valuables are limited to 30% of the contents sum insured.",
            ]),
        ]},
        {"number": "5", "heading": "Where am I covered?", "blocks": [
            ("p", "Your home at the address shown in your schedule, in the United Kingdom."),
        ]},
        {"number": "6", "heading": "What are my obligations?", "blocks": [
            ("bullets", [
                "Give us complete and accurate information when you take out and renew the policy.",
                "Tell us about any changes to your circumstances, such as building work or a change of occupancy.",
                "Take reasonable care to protect your home and prevent loss or damage.",
                "Report any claim to us within 30 days, and report theft or malicious damage to the police within 48 hours.",
            ]),
        ]},
        {"number": "7", "heading": "When and how do I pay?", "blocks": [
            ("p", "You can pay annually by debit or credit card, or in 12 monthly instalments by direct debit."),
        ]},
        {"number": "8", "heading": "When does the cover start and end?", "blocks": [
            ("p", "Cover runs for 12 months from the start date shown in your schedule."),
        ]},
        {"number": "9", "heading": "How do I cancel the contract?", "blocks": [
            ("p", "You can cancel within 14 days of receiving your documents and receive a full refund, "
                  "provided no claim has been made. After 14 days you can cancel at any time and receive "
                  "a proportionate refund, less a £25 administration fee."),
        ]},
    ],
}

# ---------------------------------------------------------------------------
# 2. Northgate Home - full Policy Wording
# ---------------------------------------------------------------------------
NORTHGATE_HOME_WORDING = {
    "doc_id": "northgate_home_wording",
    "filename": "northgate_home_wording.pdf",
    "insurer": NORTHGATE,
    "product": "Home",
    "doc_type": "Policy Wording",
    "title": "Home Insurance Policy Wording",
    "reference": "NG-HOME-PW-2026",
    "effective_date": "1 January 2026",
    "intro": (
        "Thank you for choosing Northgate Insurance. This policy wording, together with your "
        "schedule and any endorsements, forms your contract of insurance. Please read it carefully "
        "and keep it somewhere safe."
    ),
    "sections": [
        {"number": "1", "heading": "About your policy", "blocks": [
            ("p", "This policy is underwritten by Northgate Insurance plc. In return for your premium, we "
                  "will provide the cover described in this wording for the sections shown as active in "
                  "your schedule, during the period of insurance."),
            ("p", "Words shown in bold in the original wording have the meanings given in section 2 "
                  "(Definitions) wherever they appear."),
        ]},
        {"number": "2", "heading": "Definitions", "blocks": [
            ("clause", "2.1", "Buildings",
             "The home, its permanent fixtures and fittings, garages and outbuildings, swimming pools, "
             "tennis courts, drives, patios, paths, walls, gates and fences, all within the boundary "
             "of the property shown in your schedule."),
            ("clause", "2.2", "Contents",
             "Household goods and personal possessions which belong to you or for which you are "
             "legally responsible, kept in the home. Contents does not include motor vehicles, "
             "caravans, boats, or any part of the buildings."),
            ("clause", "2.3", "Escape of water",
             "Water or oil escaping from any fixed water or heating installation, washing machine, "
             "dishwasher, fridge or freezer, or fish tank."),
            ("clause", "2.4", "Excess",
             "The amount you must pay towards each claim, as set out in section 7."),
            ("clause", "2.5", "Unoccupied",
             "The home is not lived in by you or a member of your family for more than 60 consecutive "
             "days. Living in means sleeping in the home overnight."),
            ("clause", "2.6", "Valuables",
             "Jewellery, watches, items of gold, silver or other precious metals, works of art, "
             "collections of stamps, coins or medals, and furs."),
            ("clause", "2.7", "Period of insurance",
             "The period shown in your schedule, normally 12 months."),
        ]},
        {"number": "3", "heading": "General conditions", "blocks": [
            ("clause", "3.1", "Reasonable care",
             "You must take all reasonable steps to prevent loss or damage and keep the buildings "
             "in a good state of repair. We will not pay claims where loss or damage results from "
             "a failure to maintain the home."),
            ("clause", "3.2", "Changes in circumstances",
             "You must tell us as soon as possible about any change which may affect your cover, "
             "including structural alterations, the home becoming unoccupied, or anyone in the home "
             "receiving a criminal conviction."),
            ("clause", "3.3", "Unoccupancy",
             "If the home is unoccupied, cover for theft, attempted theft, escape of water and "
             "malicious damage stops from the 61st day of unoccupancy until the home is lived in "
             "again, unless we have agreed otherwise in writing."),
            ("clause", "3.4", "Fraud",
             "If any claim is fraudulent or exaggerated, we will not pay the claim, we may cancel "
             "the policy from the date of the fraudulent act, and we may report the matter to the police."),
            ("clause", "3.5", "Cancellation by you",
             "You may cancel within 14 days of receiving your documents and receive a full refund "
             "if no claim has been made. After this cooling-off period you may cancel at any time and "
             "we will refund the premium for the unexpired period, less an administration fee of £25."),
            ("clause", "3.6", "Cancellation by us",
             "We may cancel this policy by giving you at least 7 days' notice in writing, for example "
             "if you fail to pay your premium or provide information we have reasonably requested."),
        ]},
        {"number": "4", "heading": "Section A - Buildings", "blocks": [
            ("p", "We will pay for loss of or damage to the buildings caused by any of the following "
                  "insured events during the period of insurance."),
            ("table", [
                ["Insured event", "What is not covered"],
                ["Fire, smoke, explosion, lightning or earthquake", "Damage caused by smoke from fireplaces or gradual exposure to smoke"],
                ["Storm or flood", "Damage to fences, gates and hedges; damage caused by rising groundwater alone"],
                ["Escape of water", "Damage to the installation itself; damage while the home is unoccupied"],
                ["Theft or attempted theft", "Theft while the home is lent, let or sublet, unless by forcible entry"],
                ["Subsidence, heave or landslip", "Damage to drives, patios and paths unless the main building is also damaged"],
                ["Impact by vehicles, aircraft or animals", "Damage caused by pets"],
                ["Falling trees, aerials or satellite dishes", "The cost of removing a fallen tree that has not damaged the buildings"],
            ]),
            ("clause", "4.1", "Alternative accommodation",
             "If your home cannot be lived in following damage covered by this section, we will pay "
             "the reasonable cost of comparable alternative accommodation for you, your family and "
             "your pets, up to 20% of the buildings sum insured."),
            ("clause", "4.2", "Trace and access",
             "We will pay up to £5,000 for the cost of finding the source of an escape of water or "
             "oil which causes damage to the buildings, and for making good the damage caused in finding it."),
            ("clause", "4.3", "Accidental damage to buildings (optional)",
             "If your schedule shows that accidental damage cover applies, we will also pay for "
             "sudden and unexpected damage to the buildings caused by an external means, such as "
             "putting a foot through a ceiling while in the loft."),
            ("clause", "4.4", "How we settle buildings claims",
             "We will pay the cost of repair or rebuilding to the same standard, but not better, "
             "provided the buildings were in a good state of repair. If the buildings sum insured "
             "is less than the full rebuilding cost, we may reduce the amount we pay in proportion."),
        ]},
        {"number": "5", "heading": "Section B - Contents", "blocks": [
            ("p", "We will pay for loss of or damage to your contents in the home caused by any of the "
                  "insured events listed in Section A. The following limits apply."),
            ("table", [
                ["Item", "Limit"],
                ["Any single valuable (unless specified)", "£2,000"],
                ["All valuables in total", "30% of contents sum insured"],
                ["Cash and bank notes", "£500"],
                ["Contents temporarily in the garden", "£1,000"],
                ["Food in a fridge or freezer spoiled by breakdown or power failure", "£500"],
                ["Students' belongings at a term-time address", "£5,000"],
            ]),
            ("clause", "5.1", "Replacement as new",
             "We will replace items as new, except for clothing and household linen, where we will "
             "deduct an amount for wear and tear."),
            ("clause", "5.2", "Specified items",
             "Any valuable worth more than £2,000 must be listed on your schedule as a specified "
             "item, supported by a valuation dated within the last 3 years. Unspecified items above "
             "this value will only be covered up to £2,000."),
        ]},
        {"number": "6", "heading": "Section C - Personal possessions away from the home (optional)", "blocks": [
            ("p", "If your schedule shows this cover applies, we will pay for loss of or damage to "
                  "your personal possessions anywhere in the world for up to 60 days in any period "
                  "of insurance. The limit for any single item is £1,500 and for cash is £250."),
        ]},
        {"number": "7", "heading": "Excesses", "blocks": [
            ("p", "You must pay the following amount towards each claim. If more than one excess "
                  "applies to a single incident, only the highest excess will be applied."),
            ("table", [
                ["Type of claim", "Excess"],
                ["Standard excess (all claims unless stated below)", "£250"],
                ["Escape of water", "£500"],
                ["Subsidence, heave or landslip", "£1,000"],
                ["Accidental damage (optional cover)", "£250"],
                ["Personal possessions away from the home", "£100"],
            ]),
        ]},
        {"number": "8", "heading": "General exclusions", "blocks": [
            ("p", "These exclusions apply to all sections of the policy."),
            ("bullets", [
                "Wear and tear, gradual deterioration, rot, mould or rust.",
                "Damage caused by insects, vermin, birds or pets.",
                "Faulty design, workmanship or materials.",
                "War, terrorism, riot outside the UK, or nuclear contamination.",
                "Loss of data or damage caused by computer viruses or cyber attack.",
                "Any loss that happened before the policy started.",
                "Pressure waves from aircraft travelling at or above the speed of sound.",
            ]),
        ]},
        {"number": "9", "heading": "How to make a claim", "blocks": [
            ("clause", "9.1", "Telling us about a claim",
             "Call our claims line on 0800 000 0101, available 24 hours a day, or report online. "
             "You must tell us about any claim within 30 days of discovering the loss or damage."),
            ("clause", "9.2", "Theft and malicious damage",
             "You must report theft, attempted theft or malicious damage to the police within "
             "48 hours of discovery and obtain a crime reference number."),
            ("clause", "9.3", "Emergency repairs",
             "You may carry out emergency repairs to prevent further damage, up to £1,000, without "
             "asking us first. Keep the receipts and any damaged items for inspection."),
            ("clause", "9.4", "Evidence",
             "We may ask for receipts, photographs, valuations or estimates to support your claim."),
        ]},
        {"number": "10", "heading": "Complaints", "blocks": [
            ("p", "If you are unhappy with our service, please contact our Customer Relations team. "
                  "We will acknowledge your complaint within 5 working days and aim to resolve it "
                  "within 8 weeks. If you are not satisfied with our final response, or we have not "
                  "responded within 8 weeks, you may refer your complaint to the Financial Ombudsman Service."),
        ]},
    ],
}

# ---------------------------------------------------------------------------
# 3. Harbourline Home - full Policy Wording (different numbers on purpose)
# ---------------------------------------------------------------------------
HARBOURLINE_HOME_WORDING = {
    "doc_id": "harbourline_home_wording",
    "filename": "harbourline_home_wording.pdf",
    "insurer": HARBOURLINE,
    "product": "Home",
    "doc_type": "Policy Wording",
    "title": "Household Insurance Policy",
    "reference": "HL-HH-0326",
    "effective_date": "1 March 2026",
    "intro": (
        "This is your Harbourline Household Insurance policy. It sets out what is and is not "
        "covered. Your policy schedule tells you which parts you have bought and your sums insured."
    ),
    "sections": [
        {"number": "1", "heading": "Meaning of words", "blocks": [
            ("clause", "1.1", "Your home",
             "The private dwelling at the address in your schedule, including its garages and "
             "outbuildings, used only for domestic purposes."),
            ("clause", "1.2", "Escape of water",
             "A sudden escape of water from a fixed pipe, tank, radiator, boiler or domestic appliance."),
            ("clause", "1.3", "Excess",
             "The first part of any claim, which you must pay yourself. The amounts are shown in Part 5."),
            ("clause", "1.4", "Unoccupied",
             "Your home has not been lived in for more than 45 days in a row."),
            ("clause", "1.5", "High risk items",
             "Jewellery, watches, precious metals, pictures and other works of art, and collections."),
        ]},
        {"number": "2", "heading": "Your duties", "blocks": [
            ("clause", "2.1", "Looking after your home",
             "You must keep your home in good repair and take sensible steps to avoid loss or damage."),
            ("clause", "2.2", "Leaving your home empty",
             "If your home will be unoccupied for more than 45 days in a row, you must tell us. "
             "Unless we agree otherwise, we will not cover theft, escape of water, malicious damage "
             "or accidental damage while your home is unoccupied."),
            ("clause", "2.3", "Cooling-off period",
             "You have 14 days from receiving your policy to cancel and get a full refund, as long "
             "as you have not made a claim. If you cancel later, we will refund the unused part of "
             "your premium less a £30 cancellation charge."),
        ]},
        {"number": "3", "heading": "Part 3 - Your buildings", "blocks": [
            ("p", "We cover your buildings against loss or damage from fire, lightning, explosion, "
                  "storm, flood, escape of water, theft, subsidence, heave, landslip, impact and "
                  "falling trees."),
            ("clause", "3.1", "Somewhere to stay",
             "If your home cannot be lived in after an insured event, we will pay for alternative "
             "accommodation of a similar standard, up to 15% of your buildings sum insured or "
             "£50,000, whichever is lower."),
            ("clause", "3.2", "Finding a leak",
             "We will pay up to £3,000 to find where water is escaping from and to repair the "
             "damage caused while finding it."),
            ("clause", "3.3", "What we do not cover under Part 3",
             "We do not cover storm damage to gates, fences or hedges; damage caused by a gradual "
             "leak over a period of time; or subsidence caused by the settlement of new structures "
             "within 10 years of construction."),
        ]},
        {"number": "4", "heading": "Part 4 - Your contents", "blocks": [
            ("p", "We cover your contents in your home against the same causes listed in Part 3, "
                  "subject to the following limits."),
            ("table", [
                ["What is covered", "Most we will pay"],
                ["Any one high risk item", "£1,500"],
                ["All high risk items together", "25% of contents sum insured"],
                ["Money", "£300"],
                ["Contents in the open within your boundary", "£750"],
                ["Freezer food", "£300"],
                ["Belongings of a student living away from home", "£3,000"],
            ]),
            ("clause", "4.1", "New for old",
             "We will replace your contents with new items of the same quality, apart from clothes "
             "and linen, where we will take wear and tear into account."),
        ]},
        {"number": "5", "heading": "Part 5 - Your excess", "blocks": [
            ("table", [
                ["Claim type", "You pay"],
                ["Every claim unless shown below", "£350"],
                ["Escape of water", "£400"],
                ["Subsidence, heave or landslip", "£1,000"],
            ]),
        ]},
        {"number": "6", "heading": "Things we do not cover anywhere in this policy", "blocks": [
            ("bullets", [
                "Gradual damage, wear and tear, or poor maintenance.",
                "Damage by moths, insects, rodents or domestic pets.",
                "Loss which happened before your policy started.",
                "War, terrorism, radioactive contamination or sonic bangs.",
                "Cyber events, including loss of data or software.",
            ]),
        ]},
        {"number": "7", "heading": "Making a claim", "blocks": [
            ("clause", "7.1", "Contacting us",
             "Phone 0800 000 0202 or use the Harbourline app. Please tell us about your claim within "
             "14 days of the incident."),
            ("clause", "7.2", "Crime",
             "Report any theft or vandalism to the police straight away and give us the crime "
             "reference number."),
            ("clause", "7.3", "Urgent repairs",
             "You can arrange urgent repairs of up to £500 to stop further damage without our approval."),
        ]},
        {"number": "8", "heading": "If you have a complaint", "blocks": [
            ("p", "Contact our Complaints Team. If we cannot resolve your complaint within 8 weeks, "
                  "you can ask the Financial Ombudsman Service to review it."),
        ]},
    ],
}

# ---------------------------------------------------------------------------
# 4. Northgate Motor - IPID
# ---------------------------------------------------------------------------
NORTHGATE_MOTOR_IPID = {
    "doc_id": "northgate_motor_ipid",
    "filename": "northgate_motor_ipid.pdf",
    "insurer": NORTHGATE,
    "product": "Motor",
    "doc_type": "IPID",
    "title": "Car Insurance - Insurance Product Information Document",
    "reference": "NG-MOTOR-IPID-2026",
    "effective_date": "1 January 2026",
    "intro": (
        "This is a summary of Northgate Comprehensive Car Insurance. Full terms and conditions "
        "are in the Northgate Car Insurance Policy Wording."
    ),
    "sections": [
        {"number": "1", "heading": "What is this type of insurance?", "blocks": [
            ("p", "Comprehensive car insurance covers injury to other people and damage to their "
                  "property, plus loss of or damage to your own car, including fire and theft."),
        ]},
        {"number": "2", "heading": "What is insured?", "blocks": [
            ("bullets", [
                "Unlimited cover for injury to other people.",
                "Damage to other people's property up to £20,000,000.",
                "Loss of or damage to your car up to its market value.",
                "Windscreen and window glass, with a £100 excess for replacement and £25 for repair.",
                "A courtesy car while your car is repaired by one of our approved repairers.",
                "Personal belongings in the car up to £300.",
                "Cover in Europe for up to 90 days per trip.",
            ]),
        ]},
        {"number": "3", "heading": "What is not insured?", "blocks": [
            ("bullets", [
                "The compulsory excess of £300 and any voluntary excess.",
                "Theft of the car if the keys were left in or on it.",
                "Wear and tear, mechanical or electrical breakdown.",
                "Driving under the influence of alcohol or drugs.",
            ]),
        ]},
        {"number": "4", "heading": "Are there any restrictions on cover?", "blocks": [
            ("bullets", [
                "An additional excess of £250 applies if the driver is under 25.",
                "Driving other cars is third party only and only for policyholders aged 25 or over.",
            ]),
        ]},
        {"number": "5", "heading": "What are my obligations?", "blocks": [
            ("bullets", [
                "Tell us about any accident within 7 days, even if you do not wish to claim.",
                "Keep your car roadworthy and hold a valid MOT where required.",
            ]),
        ]},
        {"number": "6", "heading": "How do I cancel the contract?", "blocks": [
            ("p", "You may cancel within 14 days for a full refund if no claim has been made. "
                  "After 14 days a proportionate refund is given, less a £35 administration fee."),
        ]},
    ],
}

# ---------------------------------------------------------------------------
# 5. Northgate Motor - full Policy Wording
# ---------------------------------------------------------------------------
NORTHGATE_MOTOR_WORDING = {
    "doc_id": "northgate_motor_wording",
    "filename": "northgate_motor_wording.pdf",
    "insurer": NORTHGATE,
    "product": "Motor",
    "doc_type": "Policy Wording",
    "title": "Car Insurance Policy Wording",
    "reference": "NG-MOTOR-PW-2026",
    "effective_date": "1 January 2026",
    "intro": (
        "This policy wording, your schedule and your certificate of motor insurance together "
        "form your contract with Northgate Insurance plc. Your schedule shows the level of "
        "cover you have chosen: comprehensive, third party fire and theft, or third party only."
    ),
    "sections": [
        {"number": "1", "heading": "Definitions", "blocks": [
            ("clause", "1.1", "Approved repairer",
             "A repairer from our network that we have chosen to repair your car."),
            ("clause", "1.2", "Market value",
             "The cost of replacing your car with one of the same make, model, age, mileage and "
             "condition immediately before the loss, based on recognised motor trade guides."),
            ("clause", "1.3", "Young driver",
             "Any person driving your car who is under 25 years of age."),
            ("clause", "1.4", "Inexperienced driver",
             "Any person driving your car who has held a full driving licence for less than 2 years."),
            ("clause", "1.5", "Your car",
             "The vehicle shown on your schedule, including its standard accessories and spare parts."),
        ]},
        {"number": "2", "heading": "Section 1 - Liability to other people", "blocks": [
            ("clause", "2.1", "What we cover",
             "We will cover your legal liability for death or injury to other people without limit, "
             "and for damage to other people's property up to £20,000,000 for any one claim, "
             "arising from an accident involving your car."),
            ("clause", "2.2", "Driving other cars",
             "If your certificate allows it, you may drive another private car not owned by you or "
             "hired to you, with the owner's permission, for third party cover only. This extension "
             "applies only if you are aged 25 or over, and does not apply to young drivers named "
             "on your policy."),
        ]},
        {"number": "3", "heading": "Section 2 - Loss of or damage to your car", "blocks": [
            ("clause", "3.1", "What we cover",
             "We will pay for loss of or damage to your car caused by accident, fire, theft or "
             "attempted theft, up to its market value."),
            ("clause", "3.2", "New car replacement",
             "If your car is less than 12 months old, you are its first registered owner, and it is "
             "written off or stolen and not recovered, we will replace it with a new car of the same "
             "make and model, if one is available."),
            ("clause", "3.3", "Courtesy car",
             "While your car is being repaired by an approved repairer under this section, we will "
             "provide a small hatchback courtesy car, subject to availability. A courtesy car is not "
             "provided if your car is written off or stolen and not recovered."),
            ("clause", "3.4", "In-car entertainment",
             "We will pay up to £500 for loss of or damage to audio, navigation or entertainment "
             "equipment permanently fitted to your car."),
            ("clause", "3.5", "What we do not cover",
             "Theft or attempted theft if the keys were left in or on the car, or the car was left "
             "unlocked; wear and tear; mechanical, electrical or computer breakdown; damage to tyres "
             "caused by braking, punctures or cuts; or loss of value after a repair."),
        ]},
        {"number": "4", "heading": "Section 3 - Windscreen and glass", "blocks": [
            ("p", "We will pay to repair or replace broken glass in your car's windscreen, windows "
                  "and sunroof. Using our approved glass supplier, there is no limit to the amount "
                  "we will pay. If you use another supplier, we will pay up to £150. A windscreen "
                  "claim does not affect your no claims discount."),
        ]},
        {"number": "5", "heading": "Section 4 - Personal accident and medical expenses", "blocks": [
            ("clause", "5.1", "Personal accident",
             "We will pay £5,000 if you or your spouse or partner is accidentally killed, or suffers "
             "loss of a limb or permanent loss of sight, while travelling in or getting into or out "
             "of your car."),
            ("clause", "5.2", "Medical expenses",
             "We will pay medical expenses up to £250 for each person injured while travelling in your car."),
        ]},
        {"number": "6", "heading": "Section 5 - Personal belongings", "blocks": [
            ("p", "We will pay up to £300 for personal belongings in your car that are lost or "
                  "damaged by accident, fire, theft or attempted theft. We do not cover money, "
                  "tickets, documents, mobile phones or goods carried for business."),
        ]},
        {"number": "7", "heading": "Section 6 - Using your car abroad", "blocks": [
            ("p", "Your policy gives the same cover you have in the UK while you are driving in "
                  "any country of the European Union, plus Norway, Switzerland and Iceland, for up "
                  "to 90 days on any one trip."),
        ]},
        {"number": "8", "heading": "No claims discount", "blocks": [
            ("p", "If no claim is made during the period of insurance, your no claims discount will "
                  "increase at renewal. If a claim is made where we cannot recover our costs, your "
                  "discount will be reduced."),
            ("p", "If your schedule shows your no claims discount is protected, you may make two "
                  "claims in any three-year period before your discount is affected. Protection "
                  "does not protect the overall price of your insurance."),
        ]},
        {"number": "9", "heading": "Excesses", "blocks": [
            ("p", "The following excesses apply to claims under Section 2 (loss or damage) and "
                  "Section 3 (glass). Excesses for young and inexperienced drivers are added to "
                  "the compulsory excess."),
            ("table", [
                ["Excess", "Amount"],
                ["Compulsory excess", "£300"],
                ["Additional excess - young driver (under 25)", "£250"],
                ["Additional excess - inexperienced driver (licence held under 2 years)", "£150"],
                ["Windscreen replacement", "£100"],
                ["Windscreen repair", "£25"],
                ["Voluntary excess", "As shown on your schedule"],
            ]),
        ]},
        {"number": "10", "heading": "General exclusions", "blocks": [
            ("bullets", [
                "Any driver not named on your certificate or not holding a valid licence.",
                "Driving while over the legal alcohol limit or under the influence of drugs.",
                "Racing, rallies, track days or speed tests.",
                "Using your car for a purpose not allowed by your certificate, such as hire and reward.",
                "Deliberate damage caused by you or anyone driving with your permission.",
            ]),
        ]},
        {"number": "11", "heading": "Making a claim", "blocks": [
            ("p", "Call 0800 000 0103 as soon as possible and in any event within 7 days of the "
                  "accident or loss. Do not admit liability or offer payment to anyone. Report theft "
                  "of your car to the police immediately."),
        ]},
    ],
}

# ---------------------------------------------------------------------------
# 6. Harbourline Motor - full Policy Wording
# ---------------------------------------------------------------------------
HARBOURLINE_MOTOR_WORDING = {
    "doc_id": "harbourline_motor_wording",
    "filename": "harbourline_motor_wording.pdf",
    "insurer": HARBOURLINE,
    "product": "Motor",
    "doc_type": "Policy Wording",
    "title": "Private Car Policy",
    "reference": "HL-PC-0326",
    "effective_date": "1 March 2026",
    "intro": (
        "This is your Harbourline Private Car Policy. Your schedule and certificate show who "
        "can drive your car and what it can be used for."
    ),
    "sections": [
        {"number": "1", "heading": "Meaning of words", "blocks": [
            ("clause", "1.1", "Market value",
             "What it would cost to buy a car of the same make, model, age and condition as yours "
             "just before the loss."),
            ("clause", "1.2", "Young driver",
             "A driver who is under 25 years old."),
        ]},
        {"number": "2", "heading": "Cover for other people", "blocks": [
            ("p", "We cover your legal liability for injury to other people without limit, and "
                  "for damage to their property up to £5,000,000."),
            ("p", "This policy does not let you drive other cars. You are only covered to drive "
                  "the car shown on your schedule."),
        ]},
        {"number": "3", "heading": "Cover for your car", "blocks": [
            ("clause", "3.1", "Damage, fire and theft",
             "We will repair your car or pay its market value if it is damaged, destroyed or stolen."),
            ("clause", "3.2", "Courtesy car",
             "You will get a courtesy car while your car is being repaired by one of our network "
             "repairers. This applies to comprehensive cover only."),
            ("clause", "3.3", "Keys",
             "We will not cover theft if the keys were left in the car or the car was left unlocked."),
        ]},
        {"number": "4", "heading": "Glass cover", "blocks": [
            ("p", "We will repair or replace your windscreen and windows. You pay £90 if the glass "
                  "is replaced. There is nothing to pay if it can be repaired."),
        ]},
        {"number": "5", "heading": "Extra benefits", "blocks": [
            ("table", [
                ["Benefit", "Most we will pay"],
                ["Personal belongings", "£250"],
                ["Personal accident (death or serious injury)", "£2,500"],
                ["Medical expenses per person", "£200"],
            ]),
        ]},
        {"number": "6", "heading": "Driving in Europe", "blocks": [
            ("p", "Your full cover applies in the EU for up to 30 days on any one trip. Contact us "
                  "before travelling if you plan to go for longer."),
        ]},
        {"number": "7", "heading": "Your excess", "blocks": [
            ("table", [
                ["Excess", "You pay"],
                ["Compulsory excess", "£250"],
                ["Extra excess for young drivers", "£400"],
                ["Glass replacement", "£90"],
                ["Glass repair", "£0"],
            ]),
        ]},
        {"number": "8", "heading": "Claims", "blocks": [
            ("p", "Tell us about any accident within 48 hours by calling 0800 000 0204, even if "
                  "you do not want to make a claim."),
        ]},
    ],
}

# ---------------------------------------------------------------------------
# 7. Northgate Travel - full Policy Wording
# ---------------------------------------------------------------------------
NORTHGATE_TRAVEL_WORDING = {
    "doc_id": "northgate_travel_wording",
    "filename": "northgate_travel_wording.pdf",
    "insurer": NORTHGATE,
    "product": "Travel",
    "doc_type": "Policy Wording",
    "title": "Annual Multi-Trip Travel Insurance Policy Wording",
    "reference": "NG-TRAVEL-PW-2026",
    "effective_date": "1 January 2026",
    "intro": (
        "This policy covers you for trips taken during the period of insurance, subject to "
        "the terms, conditions and limits below."
    ),
    "sections": [
        {"number": "1", "heading": "Important information", "blocks": [
            ("clause", "1.1", "Eligibility",
             "You must be a UK resident and aged 75 or under at the start of the period of insurance."),
            ("clause", "1.2", "Trip length",
             "Each trip is covered for up to 31 consecutive days. Trips longer than 31 days are "
             "not covered at all, not even for the first 31 days."),
            ("clause", "1.3", "Pre-existing medical conditions",
             "You must tell us about any medical condition for which you have received treatment, "
             "medication or advice in the 2 years before buying this policy or booking a trip. "
             "If you do not, claims arising from that condition will not be covered."),
            ("clause", "1.4", "Winter sports",
             "Winter sports are covered for up to 17 days in any period of insurance only if your "
             "schedule shows that the winter sports premium has been paid."),
        ]},
        {"number": "2", "heading": "Summary of cover", "blocks": [
            ("table", [
                ["Section", "Maximum per person", "Excess"],
                ["Cancellation", "£5,000", "£100"],
                ["Cutting your trip short", "£5,000", "£100"],
                ["Emergency medical expenses", "£10,000,000", "£100"],
                ["Hospital benefit", "£25 per day, up to £500", "Nil"],
                ["Personal baggage", "£1,500", "£100"],
                ["Personal money", "£500 (cash £300)", "£100"],
                ["Travel delay", "£20 per 12 hours, up to £200", "Nil"],
                ["Missed departure", "£750", "£100"],
                ["Personal liability", "£2,000,000", "£100"],
            ]),
        ]},
        {"number": "3", "heading": "Section A - Cancellation and cutting your trip short", "blocks": [
            ("p", "We will pay for unused travel and accommodation costs that you have paid or "
                  "are contracted to pay, if you have to cancel or cut short your trip because of: "
                  "death, serious injury or illness of you, a travelling companion or a close "
                  "relative; you being called for jury service; your home being made uninhabitable "
                  "by fire, storm or flood; or redundancy."),
            ("p", "We will not pay if you cancel because you no longer want to travel, or because "
                  "of a pre-existing medical condition you did not tell us about."),
        ]},
        {"number": "4", "heading": "Section B - Emergency medical expenses", "blocks": [
            ("p", "We will pay up to £10,000,000 for emergency medical and hospital treatment, "
                  "and the cost of bringing you back to the UK if our medical advisers agree it "
                  "is necessary. You must contact our 24-hour emergency assistance line on "
                  "+44 20 0000 0105 before being admitted to hospital, or as soon as possible if "
                  "this is not practical."),
            ("p", "We will also pay £25 for each complete 24 hours you spend in hospital as an "
                  "inpatient abroad, up to £500."),
        ]},
        {"number": "5", "heading": "Section C - Personal baggage and money", "blocks": [
            ("p", "We will pay up to £1,500 for loss, theft or damage to your baggage. The most "
                  "we will pay for any one item, pair or set is £300, and for all valuables in "
                  "total is £400. We will deduct an amount for wear and tear."),
            ("p", "We will pay up to £500 for loss or theft of your personal money, of which no "
                  "more than £300 can be cash. If you are under 18, the cash limit is £50."),
            ("p", "You must report loss or theft to the police within 24 hours and get a written "
                  "report. Baggage lost by an airline must be reported to the airline before you "
                  "leave the airport, and you must get a property irregularity report."),
        ]},
        {"number": "6", "heading": "Section D - Travel delay and missed departure", "blocks": [
            ("p", "If your outward or return departure is delayed by more than 12 hours, we will "
                  "pay £20 for each full 12 hours of delay, up to £200. If the delay exceeds 24 "
                  "hours on your outward journey, you may instead claim for cancellation."),
            ("p", "We will pay up to £750 for extra travel and accommodation costs to reach your "
                  "destination if you miss your departure because public transport fails or the "
                  "car you are travelling in breaks down or is involved in an accident."),
        ]},
        {"number": "7", "heading": "General exclusions", "blocks": [
            ("bullets", [
                "Travel to a country or area the Foreign, Commonwealth and Development Office advises against all travel or all but essential travel.",
                "Claims arising from you being under the influence of alcohol or drugs.",
                "Taking part in dangerous activities not listed as covered.",
                "Any trip booked or started after you knew of something likely to lead to a claim.",
            ]),
        ]},
        {"number": "8", "heading": "Making a claim", "blocks": [
            ("p", "Contact our claims team within 31 days of returning home. You will need your "
                  "booking confirmation, receipts, and any police or medical reports."),
        ]},
    ],
}

# ---------------------------------------------------------------------------
# 8. Northgate - internal Claims Handling Procedure (for staff)
# ---------------------------------------------------------------------------
NORTHGATE_CLAIMS_PROCEDURE = {
    "doc_id": "northgate_claims_procedure",
    "filename": "northgate_claims_procedure.pdf",
    "insurer": NORTHGATE,
    "product": "All products",
    "doc_type": "Internal Procedure",
    "title": "Claims Handling Procedure - Personal Lines",
    "reference": "NG-OPS-CLM-004 v3.2",
    "effective_date": "1 February 2026",
    "intro": (
        "This procedure sets out how Northgate claims handlers manage personal lines claims "
        "from first notification to settlement. It applies to home, motor and travel claims. "
        "Internal use only."
    ),
    "sections": [
        {"number": "1", "heading": "Service standards", "blocks": [
            ("table", [
                ["Stage", "Standard"],
                ["Acknowledge new claim", "Within 1 working day of notification"],
                ["First contact with the customer", "Within 2 working days"],
                ["Set initial reserve", "Within 5 working days"],
                ["Review open claims", "At least every 30 days"],
                ["Payment after settlement agreed", "Within 5 working days"],
            ]),
        ]},
        {"number": "2", "heading": "First notification of loss (FNOL)", "blocks": [
            ("p", "At first notification, the handler must confirm the policy was in force on the "
                  "date of loss, check the cover section applies, and record the circumstances in "
                  "the customer's own words."),
            ("bullets", [
                "Confirm identity and policy number.",
                "Record date, time and location of the incident.",
                "Capture a crime reference number for theft or malicious damage.",
                "Ask whether any other insurance policy may cover the same loss.",
                "Advise the customer of the excess that applies.",
            ]),
        ]},
        {"number": "3", "heading": "Authority levels and referrals", "blocks": [
            ("table", [
                ["Claim value", "Who can authorise"],
                ["Up to £10,000", "Claims handler"],
                ["£10,001 to £50,000", "Senior claims handler"],
                ["Over £50,000", "Technical claims manager"],
            ]),
            ("p", "Any claim involving a suspected fraud indicator must be referred to the Counter "
                  "Fraud Unit, regardless of value."),
        ]},
        {"number": "4", "heading": "Appointing a loss adjuster", "blocks": [
            ("p", "A loss adjuster must be appointed for all subsidence claims, all buildings claims "
                  "with an estimated value over £7,500, and any contents claim over £15,000. The "
                  "adjuster should visit within 5 working days of appointment."),
        ]},
        {"number": "5", "heading": "Fraud indicators", "blocks": [
            ("p", "Handlers should look for the following indicators and refer to the Counter Fraud "
                  "Unit if two or more are present, or if any single indicator is serious."),
            ("bullets", [
                "Claim made shortly after the policy started or cover was increased.",
                "Customer is reluctant to provide documents or keeps changing their account.",
                "Receipts or valuations appear altered or come from unverifiable sources.",
                "Several recent claims on this or previous policies.",
                "Items claimed do not match the customer's described lifestyle or home.",
            ]),
        ]},
        {"number": "6", "heading": "Vulnerable customers", "blocks": [
            ("p", "If a customer shows signs of vulnerability, such as bereavement, serious illness "
                  "or financial difficulty, record this with their consent, adapt communication to "
                  "their needs, and consider a dedicated handler. Do not close a vulnerable "
                  "customer's claim without a final phone call."),
        ]},
        {"number": "7", "heading": "Settlement", "blocks": [
            ("p", "Settlement may be by repair through a network supplier, replacement through our "
                  "replacement partner, or cash payment. Where we could repair or replace through "
                  "a supplier but the customer chooses cash, we may limit the payment to the "
                  "amount it would have cost us. Always deduct the applicable excess."),
        ]},
        {"number": "8", "heading": "Declining a claim", "blocks": [
            ("p", "A claim may only be declined by a senior claims handler or above. The decline "
                  "letter must quote the exact policy wording relied on, explain the reason in plain "
                  "English, and tell the customer about their right to complain and to refer to "
                  "the Financial Ombudsman Service."),
        ]},
    ],
}

DOCUMENTS = [
    NORTHGATE_HOME_IPID,
    NORTHGATE_HOME_WORDING,
    HARBOURLINE_HOME_WORDING,
    NORTHGATE_MOTOR_IPID,
    NORTHGATE_MOTOR_WORDING,
    HARBOURLINE_MOTOR_WORDING,
    NORTHGATE_TRAVEL_WORDING,
    NORTHGATE_CLAIMS_PROCEDURE,
]

# ---------------------------------------------------------------------------
# Answer key: questions we already know the answers to.
# Used later to measure retrieval and answer accuracy.
# "type" helps us analyse which kinds of question the system struggles with.
# ---------------------------------------------------------------------------
ANSWER_KEY = [
    # Simple lookups
    {"id": "Q01", "type": "lookup", "question": "What is the standard excess on a Northgate home insurance claim?",
     "answer": "£250", "doc_id": "northgate_home_wording", "section": "7"},
    {"id": "Q02", "type": "lookup", "question": "What excess applies to an escape of water claim under the Northgate home policy?",
     "answer": "£500", "doc_id": "northgate_home_wording", "section": "7"},
    {"id": "Q03", "type": "lookup", "question": "How much will Northgate pay for trace and access on a home claim?",
     "answer": "Up to £5,000", "doc_id": "northgate_home_wording", "section": "4"},
    {"id": "Q04", "type": "lookup", "question": "What is the limit for cash under Northgate home contents cover?",
     "answer": "£500", "doc_id": "northgate_home_wording", "section": "5"},
    {"id": "Q05", "type": "lookup", "question": "What is the compulsory excess on a Northgate car insurance claim?",
     "answer": "£300", "doc_id": "northgate_motor_wording", "section": "9"},
    {"id": "Q06", "type": "lookup", "question": "How long is each trip covered for under the Northgate annual travel policy?",
     "answer": "Up to 31 consecutive days", "doc_id": "northgate_travel_wording", "section": "1"},
    {"id": "Q07", "type": "lookup", "question": "What is the emergency medical expenses limit on Northgate travel insurance?",
     "answer": "£10,000,000 per person", "doc_id": "northgate_travel_wording", "section": "2"},

    # Same question, different insurer (tests citing the right document)
    {"id": "Q08", "type": "insurer_trap", "question": "What is the standard excess on a Harbourline home insurance claim?",
     "answer": "£350", "doc_id": "harbourline_home_wording", "section": "5"},
    {"id": "Q09", "type": "insurer_trap", "question": "What is the escape of water excess under the Harbourline household policy?",
     "answer": "£400", "doc_id": "harbourline_home_wording", "section": "5"},
    {"id": "Q10", "type": "insurer_trap", "question": "How much does Harbourline pay to find a leak?",
     "answer": "Up to £3,000", "doc_id": "harbourline_home_wording", "section": "3"},
    {"id": "Q11", "type": "insurer_trap", "question": "What is the young driver excess on a Harbourline car policy?",
     "answer": "£400 extra excess for drivers under 25", "doc_id": "harbourline_motor_wording", "section": "7"},
    {"id": "Q12", "type": "insurer_trap", "question": "How many days of European driving cover does Harbourline give per trip?",
     "answer": "Up to 30 days", "doc_id": "harbourline_motor_wording", "section": "6"},

    # Conditions and exclusions
    {"id": "Q13", "type": "condition", "question": "After how many days unoccupied does Northgate stop covering theft and escape of water?",
     "answer": "From the 61st day (more than 60 consecutive days unoccupied)", "doc_id": "northgate_home_wording", "section": "3"},
    {"id": "Q14", "type": "condition", "question": "Is my car covered for theft under Northgate if I left the keys in it?",
     "answer": "No, theft is not covered if the keys were left in or on the car", "doc_id": "northgate_motor_wording", "section": "3"},
    {"id": "Q15", "type": "condition", "question": "Can a 22-year-old named driver use the driving other cars extension on a Northgate policy?",
     "answer": "No, it only applies to policyholders aged 25 or over and not to young drivers", "doc_id": "northgate_motor_wording", "section": "2"},
    {"id": "Q16", "type": "condition", "question": "Does a Harbourline car policy let me drive other cars?",
     "answer": "No, only the car shown on the schedule", "doc_id": "harbourline_motor_wording", "section": "2"},
    {"id": "Q17", "type": "condition", "question": "If my Northgate travel trip is 40 days long, am I covered for the first 31 days?",
     "answer": "No, trips longer than 31 days are not covered at all", "doc_id": "northgate_travel_wording", "section": "1"},
    {"id": "Q18", "type": "condition", "question": "Does a windscreen claim affect my Northgate no claims discount?",
     "answer": "No", "doc_id": "northgate_motor_wording", "section": "4"},

    # Procedures and deadlines
    {"id": "Q19", "type": "procedure", "question": "How quickly must I report a home insurance claim to Northgate?",
     "answer": "Within 30 days of discovering the loss or damage", "doc_id": "northgate_home_wording", "section": "9"},
    {"id": "Q20", "type": "procedure", "question": "How soon must theft be reported to the police under Northgate home insurance?",
     "answer": "Within 48 hours", "doc_id": "northgate_home_wording", "section": "9"},
    {"id": "Q21", "type": "procedure", "question": "When must I tell Harbourline about a car accident?",
     "answer": "Within 48 hours", "doc_id": "harbourline_motor_wording", "section": "8"},
    {"id": "Q22", "type": "procedure", "question": "How long do I have to submit a Northgate travel claim after returning home?",
     "answer": "Within 31 days of returning home", "doc_id": "northgate_travel_wording", "section": "8"},

    # Internal staff questions
    {"id": "Q23", "type": "internal", "question": "Who can authorise a claim worth £30,000?",
     "answer": "A senior claims handler (£10,001 to £50,000)", "doc_id": "northgate_claims_procedure", "section": "3"},
    {"id": "Q24", "type": "internal", "question": "When must a loss adjuster be appointed?",
     "answer": "All subsidence claims, buildings claims over £7,500, and contents claims over £15,000", "doc_id": "northgate_claims_procedure", "section": "4"},
    {"id": "Q25", "type": "internal", "question": "How quickly should a new claim be acknowledged?",
     "answer": "Within 1 working day of notification", "doc_id": "northgate_claims_procedure", "section": "1"},
    {"id": "Q26", "type": "internal", "question": "Who is allowed to decline a claim?",
     "answer": "A senior claims handler or above", "doc_id": "northgate_claims_procedure", "section": "8"},

    # Calculation (needs two facts combined)
    {"id": "Q27", "type": "calculation", "question": "What total excess does a 21-year-old pay on a Northgate car accidental damage claim?",
     "answer": "£550 (£300 compulsory plus £250 young driver)", "doc_id": "northgate_motor_wording", "section": "9"},

    # Not in the documents (system should say it doesn't know)
    {"id": "Q28", "type": "unanswerable", "question": "Does Northgate home insurance cover damage caused by a drone?",
     "answer": "Not stated in the documents", "doc_id": None, "section": None},
    {"id": "Q29", "type": "unanswerable", "question": "What is the Harbourline travel insurance baggage limit?",
     "answer": "Not stated - there is no Harbourline travel document", "doc_id": None, "section": None},
]
