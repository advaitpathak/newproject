# Expected comments mapping (source of truth)
expected_comments = {
    "treppdealname": "Trepp internal deal name",
    "paymentstatusofloan_delinquencystatus": "See Payment Status of Loan legend.  Codes should be populated in the following order of priority (top priority listed first).  Effective 10/1/2016 Payment status of 6 introduced to denote 120+ days delinquent; previously this was included in the payment status of 3",
    "inbankruptcy_yn": "Bankruptcy status of borrower (Y/N) Y if borrower is in bankruptcy or reorganization proceedings, else N.  If = Y, then Bankruptcy Date (L44, D16) must be populated.  If = N, then Bankruptcy Date (L44, D16) should be empty.  When borrower emerges from bankruptcy, change Y to N and remove Bankruptcy Date",
    "mostrecentfinancialindicator": "Code used to describe the period for the most recent financial data reported (interim periods), and whether or not the most recent financial information has been normalized and or annualized.  See Most Recent Financial Indicator Legend. If there are multiple properties that all have the same indicator for the same related financial statement start and end dates, print the value.  If missing any values or they are not the same, leave empty. Note - if year to date annualized (YA) is performed then the coding of YA will assume year to date normalized (YN) has been performed per CREFC Guidelines. TA = Trailing 12 months, Actual TN =Trailing 12 months normalized, YA = Year to date annualized, YN = Year to date normalized (Applies to fields 66 to 73)",
    "precedingyeardscrrollupindicator": "Code describing how DSCR is calculated for the most recent fiscal year statement available as reported by the servicer.  See DSCR Indicator Legend rule",
    "secondprecedingyeardscrrollupindicator": "Code describing how DSCR is calculated for the first consecutive year end prior to the preceding fiscal year end as reported by the servicer. See DSCR Indicator Legend rule",
    "mostrecentdscrindicator": "Code describing how DSCR is calculated for the most recent financial operating statement, as reported by the servicer, after the preceding fiscal year end statement.  See DSCR Indicator Legend",
    "noincfindicator": "Code indicating the method used to calculate net operating income or net cash flow.  See NOI/NCF Indicator Legend rule.  If multiple properties and all the same, print the value. If missing any or the values are not the same, leave empty",
    "treppdefeasancestatus": "A code indicating if a loan has or is able to be defeased. See Defeasance Status Code Legend. When a loan becomes \"Full Defeasance\", at a minimum populate Property Status (P18) with 3, populate Property Type (P13) with SE, populate Property Name with \"Defeased\", and preceding year, second preceding year and most recent operating performance related data fields, lease and tenant related data fields and property condition related data fields should be left empty. Populated with CREFC data as well as data from other sources obtained by Trepp",
    "credittenantlease": "Field designates the property as a credit tenant lease. Y= Yes  N= No",
    "propname": "Name of loan as it appears in Annex A; where Annex A is silent (i.e., multi-property loans, Trepp assigns name)",
    "address": "Address as it appears in Annex A",
    "city": "City as it appears in Annex A",
    "county": "County as it appears in Annex A, supplemented with commercially available mapping software",
    "state": "State, normalized from Annex A (multi-property loans with various states = \"vr\")",
    "zipcode": "Zip as it appears in Annex A, supplemented with commercially available mapping software",
    "msaabbreviation": "MSA abbreviation generated using commercially available mapping software",
    "normalizedpropertytype": "Trepp internally generated normalized property type",
    "propertytypeshort": "\"Short\" property type as specified in Annex A",
    "propertytypelong": "\"Detailed\" property type as specified in Annex A",
    "crefcpropertytype": "Trepp internally generated CREFC property type code",
    "originator": "Originator, seller, or contributor from Annex A; normalized by Trepp for consistency across deals – If originator is specified it is used; otherwise seller or contributor used",
    "derivednoicode": "Source of derived NOI (see Derived Credit Data Codes)",
    "derivedncfcode": "Source of derived NCF (see Derived Credit Data Codes)",
    "deriveddscr_noicode": "Source of derived DSCR (NOI) (see Derived Credit Data Codes)",
    "deriveddscr_ncfcode": "Source of derived DSCR (NCF) (see Derived Credit Data Codes)",
    "derivedltvcode": "Source of derived LTV (see Derived Credit Data Codes)",
    "derivedappraisedvaluecode": "Source of derived appraised value (see Derived Credit Data Codes)",
    "derivedoccupancycode": "Source of derived occupancy (see Derived Credit Data Codes)",
    "largesttenant": "Name of largest tenant as of securitization (unnormalized)",
    "secondlargesttenant": "Name of second largest tenant as of securitization (unnormalized)",
    "thirdlargesttenant": "Name of third largest tenant as of securitization (unnormalized)",
    "interestonly_yn": "If loan is interest only for life, then Y; if loan has more than one interest only period but is not fully interest only then P; else N",
    "ymclimittype": "Indicator determining whether YMC limit is cap or floor (\"Max\" or \"Min\")",
    "prepaymenttermsdescription": "Description (string) of prepayment restrictions",
    "armindexcode": "Index type off which ARM rate resets (see ARM Index Codes)",
    "periodicpaymentadjmaxamount": "Maximum amount ARM payment can increase or decrease in any one reset period",
    "recourse_yn": "If Annex A indicates recourse action, then Y else N",
    "maturitytype": "Whether a loan is \"balloon\" or \"self amortizing\"",
    "borrower": "Original borrower as indicated in Annex A – rarely available in Annex A",
    "hotelfranchise": "Normalized hotel name",
    "securitytype": "Fee/leasehold indicator from Annex A",
    "nonrecoverabilitydetermined": "Indicator (Y/N) as to whether the Master Servicer/Special Servicer has ceased advancing (P&I and/or Servicing) for the related mortgage loan",
    "largesttenant_current": "At a property level the name of the tenant that leases the largest square feet of the property based on the most recent annual lease rollover review.  If tenant is not occupying the space but is still paying rent, the servicer may print \"Dark\" after tenant name.  If tenant has sub-leased space, may print \"Sub-leased/name\" after tenant name.  For Office, Retail, Industrial, Other or Mixed Use property types as applicable",
    "secondlargesttenant_current": "At a property level the name of the tenant that leases the second largest square feet of the property based on the most recent annual lease rollover review.  If tenant is not occupying the space but is still paying rent, the servicer may print \"Dark\" after tenant name.  If tenant has sub-leased space, may print \"Sub-leased/name\" after tenant name.  For Office, Retail, Industrial, Other or Mixed Use property types as applicable",
    "thirdlargesttenant_current": "At a property level the name of the tenant that leases the third largest square feet of the property based on the most recent annual lease rollover review.  If tenant is not occupying the space but is still paying rent, the servicer may print \"Dark\" after tenant name.  If tenant has sub-leased space, may print \"Sub-leased/name\" after tenant name.  For Office, Retail, Industrial, Other or Mixed Use property types as applicable",
    "deriveddelinquencystatuscode": "Displays all delinquencies as reported by CREFC, in addition Trepp is deriving the foreclosure (7) and reo (9) status' which were removed with IRP 5.0.  Effective 10/1/2016, IRP 8.0 repurposed 6 (previously blank) to be 121+ days delinquent and changed 90+ days delinquent (3) to be 90-120 days delinquent.  The derived delinquency status will incorporate all 6s to show as 3s.  For actual breakout values, please reference field #40 (Payment Status of Loan)",
    "dispositiontype": "See Disposition Type Legend",
    "dispositionsubtype": "See Disposition Subtype Legend",
    "dispositioncomments": "Comments filled in by Trepp analysts",
    "acrossdealsloanidtrepp": "For loans that are pari passu (split across multiple securitizations) an integer will appear that will permit linking of loans across deals",
    "loaninotherdeals": "For loans that are pari passu (split across multiple securitizations) text will appear identifying the other securitizations where the note resides",
    "ardflag": "Anticipated Repayment Date Flag as referenced in Annex A (Y/N).  Trepp has researched additional ARD loans and if confirmed and not specified as such in the annex A, value is \"C\" for calculated.  If annex A defines as Hybrid, then will be \"H\"",
    "gurantor": "Guarantor or Sponsor as referenced in Annex A",
    "country": "Country as it appears in Annex A.  Populated only for European, Canadian and Asian deals",
    "multifamilydirected": "Populated for conduit deals which multifamily loans support class A1A",
    "delinquencystatushistory": "Delinquency status of loan for the past 12 months",
    "currentprepaymentrestriction": "Prepayment restriction as of tape date",
    "derivedicr_noi": "Derived ICR (NOI): if most recent ICR (NOI) else prior fiscal year ICR (NOI) else second prior fiscal year ICR (NOI) else securitization ICR (NOI); only full fiscal years used for most recent",
    "derivedicr_noicode": "Source of derived ICR (NOI) (see Derived Credit Data Codes)",
    "derivedicr_ncf": "Derived ICR (NCF): if most recent ICR (NCF) else prior fiscal year ICR (NCF) else second prior fiscal year ICR (NCF) else securitization ICR (NCF); only full fiscal years used for most recent",
    "derivedicr_ncfcode": "Source of derived ICR (NCF) (see Derived Credit Data Codes)",
    "loanpurpose": "Reason why the loan was originated/What the borrower used the loan for",
    "extensiontype": "Defines the type of balloon/maturity (ARD, Hard Balloon, fully amortizing, etc)",
    "l_specialservicer": "Loan Special Servicer addresses loans that are split across various deals. In such cases, Trepp assumes that the loan special servicer is the same as the special servicer of the deal with the earliest closing date",
    "derivedloanmodificationstatus": "Indication of whether the loan has been modified or whether it is modified but not modeled due to insufficient information from CREFC data (loan periodic, delinquent loan status report, remittance report, historical loan modification report)",
    "modificationdescription_trepp": "Trepp internally generated long description concerning modification",
    "modifiedloandescription": "Trepp internally generated long description concerning modification",
    "modifiedloansubordinationlevel_trepp": "Note subordinate level with structure of Hope Note",
    "modifiedhopenoteflag": "Flag used to determine whether the loan is Hope Note related",
    "modifiedloanprincipalforgiveness_trepp": "Amount of outstanding debt borrower no longer needs to return, based on modification agreement between special servicer and borrower",
    "splitloanreason": "Trepp generated reason for loan split",
    "splitloandates": "Date of loan being split (MM/YYYY). If loan is split at securitization, no date provided",
    "newlydelinquent": "Flag indicating loan intially becaming delinquent as of tape date",
    "newlysenttospecialservicing": "Flag indicating loan was initially sent to special servicing as of tape date",
    "newlyonwatchlist": "Flag indicating loan was initially put on watchlist as of tape date",
    "amortizationtype": "Trepp derived amortization classification of the loan (Balloon, Fully Amort, IO, IO then Amort, IO then Balloon)",
    "region": "Region as it appears in Annex A",
    "mortgageloanseller": "Mortgage Loan Seller as it appears in Annex A",
    "affiliatedsponsors": "Affiliated Sponsor as it appears in Annex A",
    "loantype": "Loan Type or Rate Type if available from Annex A.  Applicable for CMBS 2.0 deals and CMBS 3.0 deals",
    "securitizationtotaltrustbalance": "Total Trust Balance if available from Annex A. Applicable for CMBS 2.0 deals and CMBS 3.0 deals",
    "securitizationmasterservicer": "Master Servicer as of securitization if specified in Annex A; value is not generated if unavailable in Annex A",
    "securitizationspecialservicer": "Special Servicer as of securitization if specified in Annex A; value is not generated if unavailable in Annex A",
    "singletenantflag": "Is single tenant (Y/N)",
    "fourthlargesttenant": "Name of fourth largest tenant as of securitization (unnormalized)",
    "fifthlargesttenant": "Name of fifth largest tenant as of securitization (unnormalized)",
    "fourthlargesttenant_current": "At a property level the name of the tenant that leases the fourth largest square feet of the property based on the most recent annual lease rollover review.  If tenant is not occupying the space but is still paying rent, the servicer may print \"Dark\" after tenant name.  If tenant has sub-leased space, may print \"Sub-leased/name\" after tenant name.  For Office, Retail, Industrial, Other or Mixed Use property types as applicable",
    "fifthlargesttenant_current": "At a property level the name of the tenant that leases the fifth largest square feet of the property based on the most recent annual lease rollover review.  If tenant is not occupying the space but is still paying rent, the servicer may print \"Dark\" after tenant name.  If tenant has sub-leased space, may print \"Sub-leased/name\" after tenant name.  For Office, Retail, Industrial, Other or Mixed Use property types as applicable",
    "modifiedborrowersequity_trepp": "The equity a borrower puts into a property as part of a modification",
    "modifiedrate2_trepp": "Second modified rate based on modification report",
    "modificationdate2_trepp": "Second actual date when modification of loan terms were reflected in the Trepp model",
    "modificationdescription2_trepp": "Second Trepp internally generated long description concerning modification",
    "modifiedloan2subordinationlevel_trepp": "Second note subordinate level with structure of Hope Note",
    "modified2loanprincipalforgiveness_trepp": "Second amount of outstanding debt borrower no longer needs to return, based on modification agreement between special servicer and borrower",
    "fullmodification2notmodeledduetounavailableinfo": "Second flag indicating full modification information was not made available in CREFC data so model may not be fully changed (Y = No modification data available; P = Partial modification date available)",
    "modified2borrowersequity_trepp": "The equity a borrower puts into a property as part of a 2nd modification",
    "reasonforspecialservicertransfer": "Codes showing reason for transfer to special servicer. See Reason for SS Transfer Legend",
    "modificationbookingdate": "Date of most recent modification is booked onto the Masters servicing system and all updated information is now being reported. If no modification has occurred, then field should be left empty. For further clarification, a modification would include any material change to the existing loan documents, excluding assumptions",
    "seismiczoneflag": "Seismic Zone Flag as referenced in Annex A (Y/N)",
    "masterservicer": "The entity responsible for collection of the mortgage payments and accounting for the securitization as well as for remitting all collections and reporting all data to the Trustee/Certificate Administrator so that it can be forwarded to the certificateholders.  This entity also protects the interests of CMBS certificateholders by actively administering the mortgage loans and collateral that are the security for the bondholders' investment. See Master Servicer Legend",
    "curloanspecialservicer": "The entity responsible for the analysis, resolution and disposition of problem or defaulted loans. The Special Servicer handles collections after delinquencies, workouts, oreclosures and real estate owned (REO). The Special Servicer field should be populated for all loans to include the named Special Servicer for that loan. See Special Servicer Legend",
    "cumulativewodra": "Total WODRA amount as of the current period",
    "currentbalancepersqftorunit": "Outstanding scheduled principal balance divided by current rentable area or current number of units",
    "nameoftranchespaidbythisloan": "Name of Tranche(s) paid by this loan",
    "derivednoincfcode": "Source of derived NOI/NCF (see Derived Credit Data Codes)",
    "loanpiecesexistflag": "Indicates if loan is pari passu, part of a split loan or cross collateralized",
    "leadtransactionid": "Lead Transaction ID as outlined in the Servicing Agreement",
    "advancedbytrust_workoutdelayedreimbursementamounts_wodratoservicer_currentmonth": "Amount of shortfall to the trust related to the current month reimbursement of funds to the servicer for advances recovered via Workout Delayed Reimbursement Amounts per the PSA.  This results in a reduction to the cash flow to the trust.  Amounts in L148 should be added to cumulative field L128",
    "disclosablespecialservicingfees": "Disclosable fees paid to the Special Servicer per the applicable Servicing Agreement",
    "dealsflag": "Deals flag",
    "compendiumdealname": "Compendium Deal Name",
    "creclobloombergname": "CRE CLO Deal Bloomberg Name",
    "normalizedmsanames": "Normalized MSA name",
    "poolnum": "The Master Servicer's unique identification number assigned to each loan in the pool. If servicer loan ID is reported as duplicate, Trepp will create unique value",
    "treppdealnameloanid": "The Trepp identifier for loans",
    "bloombergdealnameloanid": "The bloomberg identifier for loans",
    "deriveddelinquencystatus": "Displays all delinquencies as reported by CREFC, in addition Trepp is deriving the foreclosure (7) and reo (9) status' which were removed with IRP 5.0.  Effective 10/1/2016, IRP 8.0 repurposed 6 (previously blank) to be 121+ days delinquent and changed 90+ days delinquent (3) to be 90-120 days delinquent.  The derived delinquency status will incorporate all 6s to show as 3s.  For actual breakout values, please reference field #40 (Payment Status of Loan)",
    "watchlist": "Flag indicating loan was initially put on watchlist as of tape date",
    "specialservice": "Loan special servicer name",
    "deliquent": "Indicator if the loan is under delinquent",
    "grace_period_loan": "Indicator if the loan is under grace period",
    "bloombergname": "Bloomberg deal name",
    "dealcategory": "bloomberg deal name",
    "loandefault": "Indicator if the loan is under default",
    "month": "Trepp internal data file month",
    "year": "Trepp internal data file year",
    "currentbeginningscheduledbalance": "Outstanding scheduled principal balance at beginning of current period (Since this comes directly from the trustee or servicers, for AB note loans it may reflect the entire note or that portion pledged to the trust). This balance should be equal to the Current Ending Scheduled Balance in the previous reporting period.  For full and partial defeasances, the balance should reflect the appropriate allocation of the balance of the non-defeased and defeased loans based on the provisions of the loan documents",
    "currentendingscheduledbalance": "The scheduled or stated principal balance for a loan (defined in the servicing agreement) as of the end of the reporting period, which is usually the current determination date.  This balance is usually determined by considering scheduled and unscheduled principal payments received during the collection period relating to the Distribution Date. A realized loss will also have an impact on this balance during the period it is reported.  For split note/loans, this should include the balance in the related trust.  For full and partial defeasances, the balance should reflect the appropriate allocation of the balance prior to the defeasance between the non-defeased and defeased loans based on the provisions of the loan documents. For AB note loans, amount is the total pledged to the trust",
    "currentnoterate": "Annualized gross rate used to calculate the current period Scheduled Interest Amount. For split loans/notes, this is the gross rate used to calculate the Scheduled Interest Amount for the split loan/note included in the related trust",
    "servicerandtrusteefeerate": "Sum of annual fee rates payable to the servicer(s)) and trustee (should not include any fees represented in fields L13 through L17 of the Loan Periodic Update File or fields S47 through S51 of the Loan Setup File in order to avoid double counting). Values are supplied by Trepp prior to first distribution of deal.  After first distribution, values are from CREFC if available, else Trepp",
    "netrate": "The Current Note Rate (L10) less the sum of the fee rates in fields L12 through L17",
    "scheduledinterestamount": "The amount of gross interest scheduled to be paid to the trust for the current distribution period based on the trust's beginning scheduled principal balance and a full month's interest accrual amount.  This amount may not be the same as the amount of gross interest scheduled to be paid by the borrower for the related payment date.  If loan has been deemed non-recoverable, then populate with zero",
    "scheduledprincipalamount": "The amount of principal to be paid to the trust for the current distribution period that represents a regularly scheduled principal payment.  The value is derived by subtracting the Scheduled Interest Amount from the Total Scheduled P&I Due.  This amount may not be the same as the amount of principal scheduled to be paid by the borrower for the related payment date.  If loan has been deemed non-recoverable, then populate with zero",
    "totalscheduledpidue": "The total amount of principal and interest due on the loan in the month corresponding to the current distribution date and should equal the sum of fields L23 and L24. If CREFC value is null, Trepp modeling payment is used; if modeling payment is a formula or vector, null is passed.  For AB note loans, null is passed",
    "unscheduledprincipalcollections": "Principal prepayments and other unscheduled payments of principal on the loan that are passed through to the certificateholders on the current distribution date.  The unscheduled amounts may include but are not limited to straight prepayments (full or partial), discounted payoffs, and/or other proceeds resulting from liquidation, condemnation, insurance settlements, etc",
    "otherprincipaladjustments": "Any other cash amounts that would cause the principal balance of the loan to be decreased or increased in the current period which are not considered Unscheduled Principal Collections and are not Scheduled Principal Amounts. Examples include adjustments necessary to synchronize the servicer's records with the securitized collateral supporting the outstanding bonds.  For modifications, refer to the definition in the respective PSAs.  A negative amount should be reported for an increase in the balance, and a positive amount should be reported for a decrease in the balance",
    "prepaymentpremiumyieldmaintenance_ymreceived": "Pursuant to the loan documents, an amount received from a borrower during the collection period in exchange for allowing a borrower to pay off a loan prior to the maturity or anticipated repayment date",
    "mostrecentnetaseramount": "Amount, as of the determination date, by which the current month principal and/or interest advances have been reduced due to an appraisal reduction event, collateral adjustment event or other similar event per the servicing agreement.  This should also include ASER recoveries (gross payments received that were previously subject to an ASER).  This value should be the mathematical change in the Cumulative ASER Amount from the prior reporting period to the current reporting period, and therefore may be negative in instances where the amount of ASER recovered exceeded the current ASER reduction",
    "cumulativeaseramount": "Cumulative amount, as of the determination date, by which the principal and/or interest advances have been reduced due to an appraisal reduction event, collateral adjustment event or other similar event per the servicing agreement.   This should also include ASER recoveries (gross payments received that were previously subject to an ASER).  This value should be the Cumulative ASER Amount from the prior reporting period plus the Most Recent Net ASER Amount for the current reporting period",
    "actualbalance": "Outstanding actual balance of the loan as of the determination date. This figure represents the legal remaining outstanding principal balance related to the borrower's mortgage note.  For partial defeasances, the balance should reflect the appropriate allocation of the balance prior to the defeasance between the non-defeased and defeased  loans based on the provisions of the loan documents",
    "totalpiadvanceoutstanding": "Total outstanding principal and interest advances made (or scheduled to be made by distribution date) by the servicer(s) as of the determination date per the servicing agreement.  Amount should also include advances reported by the special servicer in SS Total P&I Advance Outstanding (D9)",
    "totaltiadvanceoutstanding": "Total outstanding tax & insurance advances made by the servicer(s) as of the determination date per the servicing agreement.  Amount should also include advances reported by the special servicer in SS Total T&I Advance Outstanding (D10)",
    "otherexpenseadvanceoutstanding": "Total outstanding other or miscellaneous advances made by the servicer(s) as of the determination date.  This amount does not include P&I or T&I advances.  Amount should also include advances reported by the special servicer in SS Other Expense Advance Outstanding (D11)",
    "netproceedsreceivedonliquidation": "Net proceeds received on liquidation of loan to determine the Realized Loss to Trust per the servicing agreements",
    "liquidationexpense": "Expenses associated with the liquidation to be netted from the trust to determine the Realized Loss to Trust per the servicing agreement.  Should be sum of Servicer Realized Loss Template sub-totals for sections 1 through 4",
    "realizedlosstotrust": "For liquidations, a loan level calculation that is the difference between Net Proceeds (after Liquidation Expenses) and Current Beginning Scheduled Balance (L6) on the Servicer Realized Loss Template",
    "modifiednoterate": "The new initial interest rate to which the loan was modified",
    "modifiedpaymentamount": "The new initial P&I and/or interest only payment amount to which the loan was modified",
    "precedingfiscalyearrevenue": "Total revenues normalized, and annualized as applicable,  for the most recent fiscal year end statement available. If multiple properties exist and the related data is comparable, total the revenue of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "precedingfiscalyearoperatingexpenses": "Total operating expenses normalized, and annualized as applicable,  for the most recent  fiscal year end statement available.  Included are real estate taxes, insurance, management fees, utilities, and repairs and maintenance. Excluded are capital expenditures, tenant improvements, and leasing commissions.  If multiple properties exist and the related data is comparable, total the operating expenses of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "precedingfiscalyearnoi": "Total revenues less total operating expenses normalized, and annualized as applicable, before capital items and debt service for the most recent fiscal year end statement available.  If multiple properties exist and the related data is comparable, total the NOI of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "precedingfiscalyeardebtserviceamount": "Total scheduled or actual payments for the most recent fiscal year end statement available as reported by the servicer.  Payments include scheduled or actual principal and or interest as required by the loan documents.  Calculate using the current allocated percentage (P20) to get the allocated amount for each property.  If multiple properties sum the value. If missing any or if all received/consolidated, then populate using the DSCR Indicator Legend rule",
    "precedingfiscalyeardscr_noi": "A ratio of net operating income (NOI) to debt service for the most recent fiscal year end statement available as reported by the servicer. If multiple properties exist and the related data is comparable, calculate the DSCR of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule. (2)",
    "precedingfiscalyearphysicaloccupancy": "The percentage of rentable space occupied as of the most recent fiscal year end operating statement available. Should be derived from a rent roll or other document indicating occupancy, and in most cases should be within 45 days of the most recent fiscal year end financial statement. If multiple properties, populate with the weighted average based on square feet or units. If missing any, leave empty at the loan level",
    "secondprecedingfiscalyearrevenue": "Total revenues normalized, and annualized as applicable, for the first consecutive year end prior to the preceding fiscal year end statement. If multiple properties exist and the related data is comparable, total the revenue of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "secondprecedingfiscalyearoperatingexpenses": "Total operating expenses normalized, and annualized as applicable, for the first consecutive year end prior to the preceding fiscal year end statement.  Included are real estate taxes, insurance, management fees, utilities, and repairs and maintenance.  Excluded are capital expenditures, tenant improvements, and leasing commissions.  If multiple properties exist and the related data is comparable, total the operating expenses of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "secondprecedingfiscalyearnoi": "Total revenues less total operating expenses normalized, and annualized as applicable, before capital items and debt service for the first consecutive year end prior to the preceding fiscal year end statement.  If multiple properties exist and the related data is comparable, total the NOI of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "secondprecedingfiscalyeardebtserviceamount": "Total scheduled or actual payments for the first consecutive year end prior to the preceding fiscal year end statement as reported by the servicer.  Payments include scheduled or actual principal and or interest as required by the loan agreement.  Calculate using the current allocated percentage (P20) to get the allocated amount for each property.  If multiple properties sum the value. If missing any or if all received/consolidated, then populate using the DSCR Indicator Legend rule",
    "secondprecedingfiscalyeardscr_noi": "A ratio of net operating income (NOI) to debt service for the first consecutive year end prior to the preceding fiscal year end statement as reported by the servicer.  If multiple properties exist and the related data is comparable, calculate the DSCR of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "secondprecedingfiscalyearphysicaloccupancy": "The percentage of rentable space occupied as of the first consecutive year end prior to the preceding fiscal year end. Should be derived from a rent roll or other document indicating occupancy.  If multiple properties, populate with the weighted average based on square feet or units.  If missing any, leave empty at the loan level",
    "mostrecentrevenue": "Total revenues for the most recent operating statement reported by the servicer (e.g. year to date, year to date annualized, or trailing 12 months, but all normalized) after the preceding fiscal year end statement.   If multiple properties exist and the related data is comparable (same financial indicators and same financial start and end dates), total the revenue of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "mostrecentoperatingexpenses": "Total operating expenses for the most recent operating statement reported by the servicer (e.g. year to date, year to date annualized, or trailing 12 months, but all normalized) after the preceding fiscal year end statement. Included are real estate taxes, insurance, management fees, utilities and repairs and maintenance. Excluded are capital expenditures, tenant improvements, and leasing commissions.  If multiple properties exist and the related data is comparable (same financial indicators and same financial start and end dates), total the operating expenses of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "mostrecentnoi": "Total revenues less total operating expenses before capital items and debt service per the most recent operating statement reported by the servicer (e.g. year to date, year to date annualized, or trailing 12 months, but all normalized) after the preceding fiscal year end  statement.  If multiple properties exist and the related data is comparable (same financial indicators and same financial start and end dates), total the NOI of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "mostrecentdebtserviceamount": "Total scheduled or actual payments that cover the same number of months as the most recent financial operating statement reported by the servicer (e.g. year to date, year to date annualized, or trailing 12 months, but all normalized) after the preceding fiscal year end statement.  Payments include scheduled or actual principal and or interest as required by the loan documents. Calculate using the current allocated percentage (P20) to get the allocated amount for each property.  If multiple properties covering the same period (same financial statement as of start and end dates), sum the value.  If missing any or all received/consolidated then populate using the DSCR Indicator Legend rule",
    "mostrecentdscr_noi": "A ratio of net operating income (NOI) to debt service for the most recent operating statement reported by the servicer (e.g. year to date, year to date annualized, or trailing 12 months, but all normalized) after the preceding fiscal year end statement. If multiple properties exist and the related data is comparable (same financial indicators and same financial start and end dates), calculate the DSCR of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "mostrecentphysicaloccupancy": "The most recent available percentage of rentable space occupied. Should be derived from a rent roll or other document indicating occupancy consistent with most recent documentation. If property is vacant, input zero. If multiple properties, populate with the weighted average based on square feet or units.  If missing any, leave empty at the loan level",
    "mostrecentvalue": "The most recent opinion of estimated value of all properties, which could include appraisals, BPOs, or internal estimates.  This value should be the same as Valuation Amount at Contribution until a new value is obtained. This may not tie to the value used for ARA/ASER calculations if other values are obtained before or after this calculation. If multiple properties, the LPU value should equal the sum of the values from the Property File.  If missing any, leave empty.  If defeased, leave empty",
    "precedingfiscalyearncf": "Total revenues less total operating expenses and capital items normalized, and annualized as applicable, but before debt service, for the most recent fiscal year end statement available.  If multiple properties exist and the related data is comparable, total the NCF of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "precedingfiscalyeardscr_ncf": "A ratio of net cash flow (NCF) to debt service for the most recent fiscal year end statement available as reported by the servicer.   If multiple properties exist and the related data is comparable, calculate the DSCR of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "secondprecedingfiscalyearncf": "Total revenues less total operating expenses and capital items normalized, and annualized as applicable, but before debt service for the first consecutive year end prior to the preceding fiscal year end statement.  If multiple properties exist and the related data is comparable, total the NCF of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "secondprecedingfiscalyeardscr_ncf": "A ratio of net operating income (NCF) to debt service for the first consecutive year end prior to the preceding fiscal year end statement as reported by the servicer.   If multiple properties exist and the related data is comparable, calculate the DSCR of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "mostrecentncf": "Total revenues less total operating expenses and capital items but before debt service per the most recent operating statement reported by the servicer (e.g. year to date, year to date annualized, or trailing 12 months, but all normalized) after the preceding fiscal year end statement.  If multiple properties exist and the related data is comparable (same financial indicators and same financial start and end dates), total the NCF of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "mostrecentdscr_ncf": "A ratio of net cash flow (NCF) to debt service for the most recent financial operating statement reported by the servicer (e.g. year to date, year to date annualized, or trailing 12 months, but all normalized) after the preceding fiscal year end statement.  If multiple properties exist and the related data is comparable (same financial indicators and same financial start and end dates), calculate the DSCR of the underlying properties.  If multiple properties exist and comparable data is not available for all properties or if received/consolidated, populate using the DSCR Indicator Legend rule",
    "araamount": "Appraisal Reduction Amount – Generally defined in the servicing agreement.  See CREFC ARA calculation template for components of the typical calculation, however, should be calculated as required under the servicing agreement.  Until valuation is obtained, may contain requirement to calculate ARA based on a % of the scheduled principal balance or some other formula as defined in the servicing agreement",
    "latitude": "Latitude generated using commercially available mapping software – utilizes city/state/zip only; not address",
    "longitude": "Longitude generated using commercially available mapping software – utilized city/state/zip only; not address",
    "netsquarefeetatsecuritization": "Rentable area in property from Annex A",
    "cutoffloanperunit": "Securitization loan balance divided by number of units as of securitization (or rentable area if units not available)",
    "currentloanperunit": "Current loan balance divided by number of units as of securitization (or rentable area if units not available)",
    "maturityloanperunit": "Balloon balance divided by number of units as of securitization (or rentable area if units not available); balloon balance taken from Annex A, not calculated if balloon balance is not available in Annex A",
    "originalnoterate": "Original rate of loan if specified in Annex A; Note: rarely populated; securitization rate available more consistently",
    "originalbalance": "Original balance of loan.  For AB note loans, amount is the total pledged to the trust",
    "cutoffbalance": "Securitization balance of the loan; may not match Annex A for AB note loans, amount is the total pledged to the trust",
    "noterateatsecuritization": "Gross rate of loan as of securitization. If the Trepp model requires a formula for determining this rate, then this field will not be populated.",
    "scheduledballoonbalance": "Balance of loan at balloon date - from Annex A only; never calculated",
    "revenueatsecuritization": "Securitization revenues from Annex A",
    "operatingexpensesatsecuritization": "Securitization expenses from Annex A",
    "securitizationnoi": "Securitization NOI from Annex A",
    "securitizationncf": "Securitization NCF from Annex A",
    "securitzationdscr_noi": "Securitization DSCR based upon NOI from Annex A",
    "securitizationdscr_ncf": "Securitization DSCR based upon NCF from Annex A",
    "securitizationltv": "Securitization LTV from Annex A",
    "securitizationappraisedvalue": "Securitization appraised value from Annex A",
    "securitizationoccupancy": "Securitization occupancy rate from Annex A",
    "derivednoi": "Derived NOI: if most recent NOI else prior fiscal year NOI else second prior fiscal year NOI else securitization NOI; only full fiscal years used for most recent NOI",
    "derivedncf": "Derived NCF: if most recent NCF else prior fiscal year NCF else second prior fiscal year NCF else securitization NCF; only full fiscal years used for most recent",
    "deriveddscr_noi": "Derived DSCR (NOI): if most recent DSCR (NOI) else prior fiscal year DSCR (NOI) else second prior fiscal year DSCR (NOI) else securitization DSCR (NOI); only full fiscal years used for most recent",
    "deriveddscr_ncf": "Derived DSCR (NCF): if most recent DSCR (NCF) else prior fiscal year DSCR (NCF) else second prior fiscal year DSCR (NCF) else securitization DSCR (NCF); only full fiscal years used for most recent",
    "derivedltv": "Derived LTV: if most recent appraised value is populated then securitization loan balance divided by most recent appraised value *100 else securitization LTV",
    "derivedappraisedvalue": "Derived appraised value: if most recent appraised value else securitization appraised value",
    "derivedoccupancy": "Derived occupancy: if most recent physical occupancy else prior fiscal year physical occupancy else second prior fiscal year physical occupancy else securitization occupancy",
    "maturityltv": "Balloon LTV as specified in Annex A; never calculated",
    "changeinvalue": "Percent change in value from securitization appraised value to current appraised value",
    "largesttenantsquarefootage": "Square footage occupied by largest tenant as of securitization",
    "largesttenantpercent": "Percentage of square footage occupied by largest tenant as of securitization",
    "secondlargesttenantsquarefootage": "Square footage occupied by second largest tenant as of securitization",
    "secondlargesttenantpercent": "Percentage of square footage occupied by second largest tenant as of securitization",
    "thirdlargesttenantsquarefootage": "Square footage occupied by third largest tenant as of securitization",
    "thirdlargesttenantpercent": "Percentage of square footage occupied by third largest tenant as of securitization",
    "ymclimit": "Percent floor or cap of calculated YM (i.e., 1)",
    "ymcspread": "Percent to be added to treasury rate when calculating YM",
    "armmargin": "Percent to be added to Index to establish rate of ARM loan",
    "lifetimeratecap": "Maximum rate to which ARM can reset",
    "lifetimeratefloor": "Minimum rate to which ARM can reset",
    "periodicrateincreaselimit": "Maximum rate ARM can increase in any one reset period",
    "periodicratedecreaselimit": "Maximum rate ARM can decrease in any one reset period",
    "periodicpaymentadjmaxpercentage": "Maximum percent ARM payment can increase or decrease in any one reset period",
    "otherinterestadjustment": "Companion field for Other Principal Adjustments (L28) or to show unscheduled interest adjustments for the related collection period, which includes Non Recoverable interest collected",
    "cumulativeaccruedunpaidadvanceinterest": "Outstanding unpaid advance interest as of determination date",
    "totalreservebalance": "Total reserves at the loan level undisbursed as of the determination date and includes maintenance, repairs & environmental, etc, and letters of credits for reserves. Excludes tax and insurance escrows and letters of credit for tax and insurance reserves. Should be populated if Collection of Other Reserves (S77) is Y. Should equal the Ending Reserve Balance on the Reserve/LOC Report",
    "specialservicingfeeamountplusadjustments": "All Special Servicer fees paid (basis points & other collections) during the current reporting period",
    "reimbursedinterestonadvances": "Interest on advances reimbursed to the servicer(s) for the current period pursuant to the servicing agreement. This amount will impact the cash flow to the Trust for the current period",
    "workoutfeeamount": "Workout fee calculated for loans eligible for a workout fee (most often corrected mortgage loans) as per the servicing agreement. Sometimes referred to as principal recovery fee or corrected loan fee. This fee applies only to loans returned from the Special Servicer to the Master Servicer",
    "liquidationfeeamount": "Liquidation Fee calculated per the servicing agreement for each specially serviced loan that is liquidated",
    "squarefeetoflargesttenant_current": "Total square feet leased by the largest tenant in field P37. Based on the most recent annual lease roll over review",
    "squarefeetofsecond_2ndlargesttenant_current": "Total square feet leased by the 2nd largest tenant in P39. Based on the most recent annual lease roll over review",
    "squarefeetofthird_3rdlargesttenant_current": "Total square feet leased by the 3rd largest tenant in P41. Based on the most recent annual lease roll over review",
    "largesttenantpercent_current": "Percentage of square footage occupied by largest current tenant",
    "notenumber": "For loans where there is only one note, the value will be 1 (default value). If there is a modeled multiple note capital structure, all notes that are part of the trust will appear in separate lines each with a separate value",
    "paidoffamount": "Beginning balance of loan in the month it paid off or was liquidated",
    "prepaymentpenalty": "Penalty taken from loan periodic where available. Periodically supplemented through Trepp research or remittance report data",
    "lossamount": "Where loss amount in CREFC Loan Periodic file is different from the value on the remittance report, the number is taken from the most recent remittance report",
    "calculatedlosspercent": "Loss divided by initial securitized balance multiplied by 100",
    "prepaymentexposureamount": "Estimated prepayment penalty amount if loan hypothetically prepays on next distribution date. If loan is in lockout, then 0 is displayed",
    "prepaymentexposurepercent": "Estimated prepayment penalty percent if loan hypothetically prepays on next distribution date. If loan is in lockout, then 0 is displayed",
    "notepercentpledged": "Percentage of note pledged to trust",
    "currentwholeloanendingbalance": "For standard loans, this we be the same value as the Current Ending Scheduled Balance in the Loan File. For AB notes where less than 100 percent of the note is pledged, the Current Whole Loan Ending Balance will be the Current Ending Scheduled Balance divided by the NotePctPledged",
    "liquidationsalesprice": "Proceeds upon liquidation such as sales proceeds, insurance proceeds, other proceeds, and reserve/suspense balances but before broker fees and selling costs. Should be reflected on the Servicer Realized Loss Template as applicable",
    "amountsdueservicersandtrustee": "Should be the sum of items 1)a thru 1)l on the Servicer Realized Loss Template",
    "amountsheldbackforfuturepayment": "Should be the sum of items 2)a thru 2)b on the Servicer Realized Loss Template",
    "accruedinterest": "Should be the sum of 3)a thru 3)e on the Servicer Realized Loss Template",
    "additionaltrustfundexpense": "Should be the sum of 4)a thru 4)g on the Servicer Realized Loss Template",
    "currentperiodadjustmenttoloan_principal": "Should equal additional proceeds less additional expenses in the current period attributed to an adjustment to the amount of Liquidation Proceeds allocable to principal. A positive number represents additional proceeds and a negative number represents a reduction of proceeds available to the trust. The Servicer's determination that additional proceeds have been received that are allocable to principal is not a determination of whether there should be an adjustment at the bond level, which shall be determined by the governing servicing documents",
    "cumulativeadjustmentstoloan": "Cumulative additional proceeds and cumulative additional expenses after the original Realized Loss to Trust calculation. A positive number represents additional proceeds were available. This is the cumulative total of amounts reported as Current Period Adjustment to Loan – Principal plus Current Period Adjustment to Loan – Other since inception",
    "advancedbytrustnonrecoverablereimbursementstoservicer_currentmonth": "Amount of shortfall to the trust related to the current month reimbursement of funds to the servicer for non-recoverable advances. Included in this field should be Property Protection Advances that are being paid and reimbursed in the current month from general collections on non recoverable loans. This results in a reduction to the cash flow to the trust. Amounts in L122 should be added to cumulative field L128",
    "anticipatedamounttobeadvancedbytrust_lefttoreimburseservicer": "Amount still to be recovered from trust for reimbursements to servicer of non-recoverable and/or modification delayed amounts",
    "other_shortfallsrefunds": "Anything else that hits as a shortfall (reported as a negative number) or refund (reported as a positive number) that is not reported elsewhere in the Loan Periodic Update File",
    "securitizedpayment": "Total monthly scheduled principal and interest payment as of securitization",
    "modifiedrate_trepp": "Modified rate based on modification report",
    "derivedsecuritizeddebtyieldnoi": "Trepp derived Debt Yield NOI as of securitization (1)",
    "derivedcurrentdebtyieldnoi": "Trepp derived Debt Yield NOI as of tape date (1)",
    "derivedsecuritizeddebtyieldncf": "Trepp derived Debt Yield NCF as of securitization (1)",
    "derivedcurrentdebtyieldncf": "Trepp derived Debt Yield NCF as of tape date (1)",
    "securitizationparipassudebt_anote": "Pari Passu Debt - A note if available from Annex A.  Applicable for CMBS 2.0 deals and CMBS 3.0 deals",
    "fourthlargesttenantsquarefootage": "Square footage occupied by fourth largest tenant as of securitization",
    "fourthlargesttenantpercent": "Percentage of square footage occupied by fourth largest tenant as of securitization",
    "fifthlargesttenantsquarefootage": "Square footage occupied by fifth largest tenant as of securitization",
    "fifthlargesttenantpercent": "Percentage of square footage occupied by fifth largest tenant as of securitization",
    "totalexposure": "Sum of the Current Ending Scheduled Balance, Cumulative ASER Amount, Total P&I Advance Outstanding, Total T&I Advance Outstanding, Other Expense Advance Outstanding, Cumulative Accrued Unpaid Advance Interest",
    "squarefeetoffourth_4thlargesttenant_current": "Total square feet leased by the 5th largest tenant in P94.  Based on the most recent annual lease roll over review",
    "squarefeetoffifth_5thlargesttenant_current": "Total square feet leased by the 5th largest tenant in P94.  Based on the most recent annual lease roll over review",
    "advancedbytrust_cumulative": "The cumulative amounts recovered from the trust fund until collected from the borrower or other loan proceeds. Includes nonrecoverable advances and modification delayed amounts reported in L122 and L148.  Recovery would typically occur upon Liquidation or Maturity of the loan.  Items reported here will typically affect the Realized Loss forms of the loan",
    "currentperiodadjustmenttoloan_other": "Should equal additional proceeds less additional expenses in the current period not attributed to an adjustment to the amount of Liquidation Proceeds allocable to principal. A positive number represents additional proceeds and a negative number represents a reduction of proceeds available to the trust. The Servicer's determination that additional proceeds have been received that are not allocable to principal is not a determination of whether there should be an adjustment at the bond level, which shall be determined by the governing servicing documents",
    "derivedltv2": "Derived LTV#2: Outstanding scheduled principal balance at end of current period divided by appraisal * 100 (see Derived LTV #2 Code for appraisal source)",
    "currentnetrentablesquarefeet": "The current net rentable square feet area of a property as of the determination date.  This field should be utilized for Office, Retail, Industrial, Warehouse, and Mixed Use properties.  If there are multiple properties, and all the same Property Type, sum the values.  If not all the same Property Type or if any are missing, then leave field empty",
    "pctsqfeetexpiring1_12months": "The percentage of leases, as reflected on the rent roll utilized for the Date Lease Rollover Review, that are expiring in months 1 to 12.  Months 1 to 12 should include month to month leases.  This field should be derived using the total net rentable square feet reflected on the rent roll as the denominator (not the Net Rentable Square Fee at Contribution).  The vacancy percentage should not be included in this field. This analysis applies to Property Types - RT, IN, OF, MU, OT",
    "pctsqfeetexpiring13_24months": "The percentage of leases, as reflected on the rent roll utilized for the Date Lease Rollover Review, that are expiring in 13 to 24 months.  This field should be derived using the total net rentable square feet reflected on the rent roll as the denominator (not the Net Rentable Square Fee at Contribution).  The vacancy percentage should not be included in this field.  This analysis applies to Property Types - RT, IN, OF, MU, OT",
    "pctsqfeetexpiring25_36months": "The percentage of leases, as reflected on the rent roll utilized for the Date Lease Rollover Review, that are expiring in 25 to 36 months.  This field should be derived using the total net rentable square feet reflected on the rent roll as the denominator (not the Net Rentable Square Fee at Contribution).  The vacancy percentage should not be included in this field.  This analysis applies to Property Types - RT, IN, OF, MU, OT",
    "pctsqfeetexpiring37_48months": "The percentage of leases, as reflected on the rent roll utilized for the Date Lease Rollover Review, that are expiring in 37 to 48 months.  This field should be derived using the total net rentable square feet reflected on the rent roll as the denominator (not the Net Rentable Square Fee at Contribution).  The vacancy percentage should not be included in this field.  This analysis applies to Property Types - RT, IN, OF, MU, OT",
    "pctsqfeetexpiring49_months": "The percentage of leases, as reflected on the rent roll utilized for the Date Lease Rollover Review, that are expiring in 49+ months.  This field should be derived using the total net rentable square feet reflected on the rent roll as the denominator (not the Net Rentable Square Fee at Contribution).  The vacancy percentage should not be included in this field.  This analysis applies to Property Types - RT, IN, OF, MU, OT",
    "derivednoincf": "Trepp derived NOI/NCF value",
    "cumulativenonrecoverableinterest": "Subtotal of Non Recoverable Interest not yet paid to the Trust.  This value should be the Cumulative Non Recoverable Interest from the prior reporting period plus the Current Non Recoverable Interest for the current reporting period.  This value should not be impacted by amounts in L128 or L122.  For liquidations / payoffs if the prior amounts are not fully recovered the amount remaining should be populated in the month of liquidation and then be blank in subsequent months",
    "largesttenantpercent_current2": "The area percentage of the current second largest tenant",
    "largesttenantpercent_current3": "The area percentage of the current third largest tenant",
    "largestcurrenttenantpercent4": "The area percentage of the current fourth largest tenant",
    "largestcurrenttenantpercent5": "The area percentage of the current fifth largest tenant",
    "distributiondate": "Date on which funds are distributed to certificateholders for a particular period as defined in the servicing agreement. (YYYYMMDD)",
    "filedate": "Trepp internal data file update date",
    "paidthroughdate": "Date the loan's scheduled principal and interest is paid through as of the determination date. One frequency less than the due date for the loan's next scheduled payment.  For split loans/notes, this is the date the scheduled principal and interest for the split loan/note piece has been paid through. (YYYYMMDD)",
    "maturitydate": "Date final scheduled payment is due per the loan documents. Not the same as anticipated repayment date related to hyper-amortization loans.  If the loan has been defeased and the loan agreement provided for, or the servicer has consented to, prepayment prior to maturity in connection with a defeasance, this represents the date the Trust can expect full repayment.  The borrower may have the right to pre-pay the defeased loan prior to the final scheduled payment date in accordance with the loan documents. (YYYYMMDD)",
    "liquidationprepaymentdate": "The effective date on which an unscheduled principal payment or liquidation proceeds are received. (YYYYMMDD)",
    "liquidationprepaymentcode": "Code assigned to any unscheduled principal payments or liquidation proceeds received during the collection period. See Liquidation/Prepayment Code Legend",
    "foreclosurestartdate": "The date on which foreclosure proceedings were initiated, or alternative processes such as deed in lieu of foreclosure, were initiated against or agreed by the borrower.  If multiple properties, then use the first date the first property started foreclosure proceedings.  The field will be reported as blank if such actions were never initiated, or if initiated actions are withdrawn, dismissed or otherwise terminated. (YYYYMMDD)",
    "reodate": "The date on which title to (or an alternative form of effective control and ability to dispose of) the collateral property was obtained.  For loan level reporting, if multiple properties have the same date then print that date, otherwise print the earliest date. (YYYYMMDD)",
    "bankruptcydate": "Date of borrower bankruptcy (YYYYMMDD) If \"In Bankruptcy\" flag (L41, D13) = N, then leave empty",
    "dateoflastmodification": "Date most recent modification/forbearance is effective.  If no modification/forbearance has occurred, then field should be left empty.  For further clarification, a modification/forbearance would include any material change to the existing loan documents, excluding assumptions. (YYYYMMDD)",
    "modificationcode": "Type of loan modification. See Modification Code Legend (US deals) and EUROPEAN Modification Code Legend",
    "precedingfiscalyearfinancialasofdate": "The end date for the most recent, hard copy fiscal year end statement available.  (Note - the end date of the operating statement from the borrower used to annualize should be reported.)  If multiple properties and all the same, then print the date. If missing any, leave empty. (YYYYMMDD)",
    "secondprecedingfiscalyearfinancialasofdate": "The end date of the hard copy operating statement that relates to the the first consecutive year end prior to the preceding fiscal year end statement. (Note - the end date of the operating statement from the borrower used to annualize should be reported.) If multiple properties and all the same, print the date.  If missing any, leave empty. (YYYYMMDD)",
    "mostrecentfinancialasofstartdate": "The first day of the period for the most recent, hard copy operating statement (e.g. year to date or trailing 12 months) after the preceding fiscal year end statement.  (Note - the beginning and end date of the operating statement from the borrower used to annualize should be reported.)  If multiple properties and all the same start and end date, print start date.  If missing any, leave empty. (YYYYMMDD)",
    "mostrecentfinancialasofenddate": "The last day of the period for the most recent, hard copy operating statement (e.g. year to date or trailing 12 months) after the preceding fiscal year end statement. (Note - the beginning and end date of the operating statement from the borrower used to annualize should be reported.) If multiple properties and all the same start and end date, print the end date.  If missing any, leave empty. (YYYYMMDD)",
    "mostrecentvaluationdate": "The date the most recent opinion of estimated value (as reported in Most Recent Value L75, P25, D26) was effective.  If multiple properties and all the same date, print date.  If missing any, leave empty.  If defeased, leave empty. (YYYYMMDD)",
    "workoutstrategy": "The code assigned that best describes the steps being taken to resolve the loan.  Specific codes apply.  See Workout Strategy Legend for US/Canadian deals and See EUROPEAN Workout Strategy Legend for European deals",
    "mostrecentspecialservicertransferdate": "The date a loan becomes a \"specially serviced loan\", which is the date of the transfer letter, e-mail, etc. provided by the Master Servicer which is accepted by the Special Servicer.  Note: If the loan has had multiple transfers, this should be the last date transferred to special servicing. (YYYYMMDD)",
    "mostrecentmasterservicerreturndate": "The date a loan becomes a \"corrected mortgage loan\", which is the date of the return letter, email, etc. provided by the Special Servicer which is accepted by the Master Servicer.  Note: If the loan has had multiple transfers, this should be the last date returned to the Master Servicer from the Special Servicer. (YYYYMMDD)",
    "numberofproperties": "Number of properties from Annex A",
    "aradate": "The determination date corresponding to the month when the ARA is calculated.  The frequency of the ARA calculation as per the servicing agreement (annually, monthly, or upon receipt of a new appraisal) should correlate to the timing of any change in the ARA Date",
    "treppmasterloanid": "Trepp Master Loan ID (Key Field)",
    "msacode": "MSA code generated using commercially available mapping software",
    "units": "Number of units in property from Annex A (i.e., rooms, beds, pads, etc)",
    "yearbuilt": "Year property was built from Annex A (If multiple years provided in Annex A, Trepp uses earliest year)",
    "originationdate": "Origination date of loan if specified in Annex A; value generated by Trepp if unavailable in Annex A (YYYYMMDD)",
    "originaltermofloan": "Original term of loan as specified in Annex A – may be adjusted if loan is modified",
    "originalamortization": "Amortization term as specified in Annex A; for step payment loans or odd amortization, values of 999 will appear; IO periods are added in – i.e. loan with 360 months of a term following 24 months of IO will show a term of 384; may be adjusted if loan is modified",
    "remainingtermatsecuritization": "Remaining term to the lesser of the maturity date or ARD date as specified in Annex A",
    "maturitydateatsecuritization": "Maturity date as specified in Annex A (Note: may differ from CREFC maturity date (field 12) – will not be modified if loan terms are modified) (YYYYMMDD)",
    "remainingterm": "Current remaining term to lesser of maturity date or ARD date; may be inconsistent with CREFC maturity date (field 12)",
    "securitizationappraisedvaluedate": "Date of securitization appraised value from Annex A (YYYYMMDD)",
    "securitizationoccupancydate": "Date of securitization occupancy rate from Annex A (YYYYMMDD)",
    "derivedappraisedvaluedate": "Date of derived appraised value (YYYYMMDD)",
    "derivedoccupancydate": "Date of derived occupancy (YYYYMMDD)",
    "expirationdateoflargesttenantslease": "Expiration date of lease of largest tenant as of securitization (YYYYMMDD)",
    "expirationdateofsecondlargesttenantslease": "Expiration date of lease of second largest tenant as of securitization (YYYYMMDD)",
    "expirationdateofthirdlargesttenantslease": "Expiration date of lease of third largest tenant as of securitization (YYYYMMDD)",
    "numberofinterestonlyperiods": "Number of interest only periods from origination of loan (static value) – may change if loan is modified",
    "interestaccrualmethodcode": "Interest basis of loan (see Payment Basis Codes)",
    "prepaymentlock_outendperiod": "Number of lockout periods from origination of loan (static value)",
    "firstyieldmaintenanceperiod": "Number of periods from origination of loan to first yield maintenance (YM) period (static value)",
    "yieldmaintenanceendperiod": "Number of periods from origination of loan to last YM period (static value)",
    "firstpremiumperiod": "Number of periods from origination of loan to first premium period (static value)",
    "prepaymentpremiumendperiod": "Number of periods from origination of loan to last premium period (static value)",
    "paymentfrequency": "Frequency of loan payments",
    "rateresetfrequency_months": "Number of periods between rate resets (Note: not same as frequency; 12 = annual reset)",
    "paymentresetfrequency_months": "Number of periods between payment resets (Note: not same as frequency; 12 = annual reset )",
    "monthstonextratereset": "Number of periods until next rate reset",
    "monthstonextpaymentreset": "Number of periods until next payment reset",
    "cross_collaterizedloangrouping": "Indicator of loans that are cross collateralized (Example:  loans 1 and 44 from Annex A are cross collateralized as are loans 4 and 47).  First pair will be assigned value of 1; second pair assigned value of 2",
    "monthsdelinquent": "Number of months from paid through date to current collateral cutoff date.  Change effective 5/1/03, loans are now flagged with \"1\" once they are 60 days delinquent, not 30 days delinquent",
    "dateaddedtoservicerwatchlist": "The most recent determination date that a loan was placed on the Servicer Watchlist. If a loan is not on the Servicer Watchlist or comes off the Servicer Watchlist, the field should be empty.  If a loan subsequently comes back on the Servicer Watchlist, input the new determination date. (YYYYMMDD)",
    "calculatedmaturitydate": "Derived from the Trepp remaining term for modeling purposes (which uses the anticipated repayment date for ARD loans).  This change will also reflect all known modifications as the Trepp remaining term for modeling purposes is modified for loan modifications",
    "dateofleaseexpirationoflargesttenant_current": "Expiration date of lease of largest current tenant (YYYYMMDD)",
    "dateofleaseexpirationofsecond_2ndlargesttenant_current": "Expiration date of lease of second largest current tenant (YYYYMMDD)",
    "dateofleaseexpirationofthird_3rdlargesttenant_current": "Expiration date of lease of third largest current tenant (YYYYMMDD)",
    "dispositiondate": "Liquidation/prepayment date from CREFC Loan Periodic file if available, else uses the distribution date when loan was paid off/liquidated",
    "lastpaidthrudate": "Paid through date of loan reported in CREFC Loan Periodic in month prior to loan paying off/liquidating",
    "monthstorecover": "Number of months between disposition date and last paid through date. (Only populated for loans where disposition type is a loss)",
    "dateofcurrentperiodadjustmenttoloan": "Distribution Date in which additionally proceeds or expenses have been received after the original Realized Loss",
    "numberofnotes": "Total number of notes in the whole loan capital structure that are modeled (includes both pledged and non-pledged notes).  For loans which we do not model the whole loan capital structure, value will be null",
    "delinquencycount": "Number of times loan has been delinquent",
    "currentmonthlockout": "Lockout periods as of tape date",
    "currentmonthymc": "YMC periods as of tape date",
    "currentmonthprepaymentpremium": "Prepayment Premium as of tape date",
    "securitizedmonthlockout": "Lockout periods as of securitization",
    "securitizedmonthymc": "YMC periods as of securitization",
    "securitizedmonthprepaymentpremium": "Prepayment Premium as of securitization",
    "firstcallperiod": "First period defeasance option can occur",
    "periodspastmaturity": "Number of periods loan is past maturity date",
    "renovationyearatsecuritization": "Year property was renovated from Annex A (If multiple years provided in Annex A, Trepp uses latest year)",
    "modificationdate_trepp": "Actual date when modification of loan terms were reflected in the Trepp model",
    "modifiedinterestonlyperiodchange": "Change in interest only periods due to modification",
    "modifiedoriginaltermchange": "Change in original term due to modification",
    "splitloanidentifier": "Servicer Loan ID of original loan that was split",
    "seasoning": "Loan age as of tape date",
    "fifthlargesttenantleaseexpirationdate": "Expiration date of lease of fifth largest tenant as of securitization (YYYYMMDD)",
    "dateofleaseexpirationoffourth_4thlargesttenant_current": "Expiration date of lease of fourth largest current tenant (YYYYMMDD)",
    "dateofleaseexpirationoffifth_5thlargesttenant_current": "Expiration date of lease of fifth largest current tenant (YYYYMMDD)",
    "modificationexecutiondate": "Date of most recent modification was executed by the Special Servicer. If no modification has occurred, then field should be left empty. For further clarification, a modification would include any material change to the existing loan documents, excluding assumptions",
    "currentnumberofunitsbedsrooms": "The current number of units/beds/rooms of a property as of the determination date. This field should be utilized for Multifamily, Cooperative Housing, Mobile Home Parks and Self Storage (units), Healthcare (beds), and Lodging (rooms). If there are multiple properties, and all the same Property Type, sum the values. If not all the same Property Type or if any are missing, then leave field empty",
    "firstopendate": "First date the loan is eligible to prepay without incurring any penalities",
    "treppderivedmsaranking": "Trepp Derived MSA Rank by population",
    "remainingperiodsuntilfirstdefeasible": "Number of periods until Defeasance can occur",
    "modificationindicator": "If the loan has been modified or subject to a forebearance, this field should have a Y, otherwise an N should be populated (1=Y, 0=N)",
    "compendiumdealflag": "Compendium Deal Flag",
    "isprivateflag": "Indicator if the loan is public or private"
}

# Actual schema definition
actual_schema = [
  {
    "Name": "treppdealname",
    "Type": "string"
  },
  {
    "Name": "distributiondate",
    "Type": "date"
  },
  {
    "Name": "currentbeginningscheduledbalance",
    "Type": "double"
  },
  {
    "Name": "currentendingscheduledbalance",
    "Type": "double"
  },
  {
    "Name": "paidthroughdate",
    "Type": "date"
  },
  {
    "Name": "currentnoterate",
    "Type": "double"
  },
  {
    "Name": "maturitydate",
    "Type": "date"
  },
  {
    "Name": "servicerandtrusteefeerate",
    "Type": "double"
  },
  {
    "Name": "netrate",
    "Type": "double"
  },
  {
    "Name": "scheduledinterestamount",
    "Type": "double"
  },
  {
    "Name": "scheduledprincipalamount",
    "Type": "double"
  },
  {
    "Name": "totalscheduledpidue",
    "Type": "double"
  },
  {
    "Name": "unscheduledprincipalcollections",
    "Type": "double"
  },
  {
    "Name": "otherprincipaladjustments",
    "Type": "double"
  },
  {
    "Name": "liquidationprepaymentdate",
    "Type": "date"
  },
  {
    "Name": "prepaymentpremiumyieldmaintenance_ymreceived",
    "Type": "double"
  },
  {
    "Name": "liquidationprepaymentcode",
    "Type": "bigint"
  },
  {
    "Name": "mostrecentnetaseramount",
    "Type": "double"
  },
  {
    "Name": "cumulativeaseramount",
    "Type": "double"
  },
  {
    "Name": "actualbalance",
    "Type": "double"
  },
  {
    "Name": "totalpiadvanceoutstanding",
    "Type": "double"
  },
  {
    "Name": "totaltiadvanceoutstanding",
    "Type": "double"
  },
  {
    "Name": "otherexpenseadvanceoutstanding",
    "Type": "double"
  },
  {
    "Name": "paymentstatusofloan_delinquencystatus",
    "Type": "string"
  },
  {
    "Name": "inbankruptcy_yn",
    "Type": "string"
  },
  {
    "Name": "foreclosurestartdate",
    "Type": "date"
  },
  {
    "Name": "reodate",
    "Type": "date"
  },
  {
    "Name": "bankruptcydate",
    "Type": "date"
  },
  {
    "Name": "netproceedsreceivedonliquidation",
    "Type": "double"
  },
  {
    "Name": "liquidationexpense",
    "Type": "double"
  },
  {
    "Name": "realizedlosstotrust",
    "Type": "double"
  },
  {
    "Name": "dateoflastmodification",
    "Type": "date"
  },
  {
    "Name": "modificationcode",
    "Type": "bigint"
  },
  {
    "Name": "modifiednoterate",
    "Type": "double"
  },
  {
    "Name": "modifiedpaymentamount",
    "Type": "double"
  },
  {
    "Name": "precedingfiscalyearrevenue",
    "Type": "double"
  },
  {
    "Name": "precedingfiscalyearoperatingexpenses",
    "Type": "double"
  },
  {
    "Name": "precedingfiscalyearnoi",
    "Type": "double"
  },
  {
    "Name": "precedingfiscalyeardebtserviceamount",
    "Type": "double"
  },
  {
    "Name": "precedingfiscalyeardscr_noi",
    "Type": "double"
  },
  {
    "Name": "precedingfiscalyearphysicaloccupancy",
    "Type": "double"
  },
  {
    "Name": "precedingfiscalyearfinancialasofdate",
    "Type": "date"
  },
  {
    "Name": "secondprecedingfiscalyearrevenue",
    "Type": "double"
  },
  {
    "Name": "secondprecedingfiscalyearoperatingexpenses",
    "Type": "double"
  },
  {
    "Name": "secondprecedingfiscalyearnoi",
    "Type": "double"
  },
  {
    "Name": "secondprecedingfiscalyeardebtserviceamount",
    "Type": "double"
  },
  {
    "Name": "secondprecedingfiscalyeardscr_noi",
    "Type": "double"
  },
  {
    "Name": "secondprecedingfiscalyearphysicaloccupancy",
    "Type": "double"
  },
  {
    "Name": "secondprecedingfiscalyearfinancialasofdate",
    "Type": "date"
  },
  {
    "Name": "mostrecentrevenue",
    "Type": "double"
  },
  {
    "Name": "mostrecentoperatingexpenses",
    "Type": "double"
  },
  {
    "Name": "mostrecentnoi",
    "Type": "double"
  },
  {
    "Name": "mostrecentdebtserviceamount",
    "Type": "double"
  },
  {
    "Name": "mostrecentdscr_noi",
    "Type": "double"
  },
  {
    "Name": "mostrecentphysicaloccupancy",
    "Type": "double"
  },
  {
    "Name": "mostrecentfinancialasofstartdate",
    "Type": "date"
  },
  {
    "Name": "mostrecentfinancialasofenddate",
    "Type": "date"
  },
  {
    "Name": "mostrecentvaluationdate",
    "Type": "date"
  },
  {
    "Name": "mostrecentvalue",
    "Type": "double"
  },
  {
    "Name": "workoutstrategy",
    "Type": "bigint"
  },
  {
    "Name": "mostrecentspecialservicertransferdate",
    "Type": "date"
  },
  {
    "Name": "mostrecentmasterservicerreturndate",
    "Type": "date"
  },
  {
    "Name": "mostrecentfinancialindicator",
    "Type": "string"
  },
  {
    "Name": "numberofproperties",
    "Type": "bigint"
  },
  {
    "Name": "precedingyeardscrrollupindicator",
    "Type": "string"
  },
  {
    "Name": "secondprecedingyeardscrrollupindicator",
    "Type": "string"
  },
  {
    "Name": "mostrecentdscrindicator",
    "Type": "string"
  },
  {
    "Name": "noincfindicator",
    "Type": "string"
  },
  {
    "Name": "precedingfiscalyearncf",
    "Type": "double"
  },
  {
    "Name": "precedingfiscalyeardscr_ncf",
    "Type": "double"
  },
  {
    "Name": "secondprecedingfiscalyearncf",
    "Type": "double"
  },
  {
    "Name": "secondprecedingfiscalyeardscr_ncf",
    "Type": "double"
  },
  {
    "Name": "mostrecentncf",
    "Type": "double"
  },
  {
    "Name": "mostrecentdscr_ncf",
    "Type": "double"
  },
  {
    "Name": "treppdefeasancestatus",
    "Type": "string"
  },
  {
    "Name": "araamount",
    "Type": "double"
  },
  {
    "Name": "aradate",
    "Type": "date"
  },
  {
    "Name": "credittenantlease",
    "Type": "string"
  },
  {
    "Name": "treppmasterloanid",
    "Type": "bigint"
  },
  {
    "Name": "propname",
    "Type": "string"
  },
  {
    "Name": "address",
    "Type": "string"
  },
  {
    "Name": "city",
    "Type": "string"
  },
  {
    "Name": "county",
    "Type": "string"
  },
  {
    "Name": "state",
    "Type": "string"
  },
  {
    "Name": "zipcode",
    "Type": "string"
  },
  {
    "Name": "msacode",
    "Type": "bigint"
  },
  {
    "Name": "msaabbreviation",
    "Type": "string"
  },
  {
    "Name": "latitude",
    "Type": "double"
  },
  {
    "Name": "longitude",
    "Type": "double"
  },
  {
    "Name": "normalizedpropertytype",
    "Type": "string"
  },
  {
    "Name": "propertytypeshort",
    "Type": "string"
  },
  {
    "Name": "propertytypelong",
    "Type": "string"
  },
  {
    "Name": "crefcpropertytype",
    "Type": "string"
  },
  {
    "Name": "units",
    "Type": "bigint"
  },
  {
    "Name": "netsquarefeetatsecuritization",
    "Type": "double"
  },
  {
    "Name": "cutoffloanperunit",
    "Type": "double"
  },
  {
    "Name": "currentloanperunit",
    "Type": "double"
  },
  {
    "Name": "maturityloanperunit",
    "Type": "double"
  },
  {
    "Name": "yearbuilt",
    "Type": "bigint"
  },
  {
    "Name": "originator",
    "Type": "string"
  },
  {
    "Name": "originationdate",
    "Type": "date"
  },
  {
    "Name": "originalnoterate",
    "Type": "double"
  },
  {
    "Name": "originaltermofloan",
    "Type": "bigint"
  },
  {
    "Name": "originalamortization",
    "Type": "bigint"
  },
  {
    "Name": "originalbalance",
    "Type": "double"
  },
  {
    "Name": "cutoffbalance",
    "Type": "double"
  },
  {
    "Name": "noterateatsecuritization",
    "Type": "double"
  },
  {
    "Name": "remainingtermatsecuritization",
    "Type": "bigint"
  },
  {
    "Name": "maturitydateatsecuritization",
    "Type": "date"
  },
  {
    "Name": "scheduledballoonbalance",
    "Type": "double"
  },
  {
    "Name": "remainingterm",
    "Type": "bigint"
  },
  {
    "Name": "revenueatsecuritization",
    "Type": "double"
  },
  {
    "Name": "operatingexpensesatsecuritization",
    "Type": "double"
  },
  {
    "Name": "securitizationnoi",
    "Type": "double"
  },
  {
    "Name": "securitizationncf",
    "Type": "double"
  },
  {
    "Name": "securitzationdscr_noi",
    "Type": "double"
  },
  {
    "Name": "securitizationdscr_ncf",
    "Type": "double"
  },
  {
    "Name": "securitizationltv",
    "Type": "double"
  },
  {
    "Name": "securitizationappraisedvalue",
    "Type": "double"
  },
  {
    "Name": "securitizationappraisedvaluedate",
    "Type": "date"
  },
  {
    "Name": "securitizationoccupancy",
    "Type": "double"
  },
  {
    "Name": "securitizationoccupancydate",
    "Type": "date"
  },
  {
    "Name": "derivednoi",
    "Type": "double"
  },
  {
    "Name": "derivednoicode",
    "Type": "string"
  },
  {
    "Name": "derivedncf",
    "Type": "double"
  },
  {
    "Name": "derivedncfcode",
    "Type": "string"
  },
  {
    "Name": "deriveddscr_noi",
    "Type": "double"
  },
  {
    "Name": "deriveddscr_noicode",
    "Type": "string"
  },
  {
    "Name": "deriveddscr_ncf",
    "Type": "double"
  },
  {
    "Name": "deriveddscr_ncfcode",
    "Type": "string"
  },
  {
    "Name": "derivedltv",
    "Type": "double"
  },
  {
    "Name": "derivedltvcode",
    "Type": "string"
  },
  {
    "Name": "derivedappraisedvalue",
    "Type": "double"
  },
  {
    "Name": "derivedappraisedvaluedate",
    "Type": "date"
  },
  {
    "Name": "derivedappraisedvaluecode",
    "Type": "string"
  },
  {
    "Name": "derivedoccupancy",
    "Type": "double"
  },
  {
    "Name": "derivedoccupancydate",
    "Type": "date"
  },
  {
    "Name": "derivedoccupancycode",
    "Type": "string"
  },
  {
    "Name": "maturityltv",
    "Type": "double"
  },
  {
    "Name": "changeinvalue",
    "Type": "double"
  },
  {
    "Name": "largesttenant",
    "Type": "string"
  },
  {
    "Name": "largesttenantsquarefootage",
    "Type": "double"
  },
  {
    "Name": "largesttenantpercent",
    "Type": "double"
  },
  {
    "Name": "expirationdateoflargesttenantslease",
    "Type": "date"
  },
  {
    "Name": "secondlargesttenant",
    "Type": "string"
  },
  {
    "Name": "secondlargesttenantsquarefootage",
    "Type": "double"
  },
  {
    "Name": "secondlargesttenantpercent",
    "Type": "double"
  },
  {
    "Name": "expirationdateofsecondlargesttenantslease",
    "Type": "date"
  },
  {
    "Name": "thirdlargesttenant",
    "Type": "string"
  },
  {
    "Name": "thirdlargesttenantsquarefootage",
    "Type": "double"
  },
  {
    "Name": "thirdlargesttenantpercent",
    "Type": "double"
  },
  {
    "Name": "expirationdateofthirdlargesttenantslease",
    "Type": "date"
  },
  {
    "Name": "interestonly_yn",
    "Type": "string"
  },
  {
    "Name": "numberofinterestonlyperiods",
    "Type": "bigint"
  },
  {
    "Name": "interestaccrualmethodcode",
    "Type": "bigint"
  },
  {
    "Name": "prepaymentlock_outendperiod",
    "Type": "bigint"
  },
  {
    "Name": "firstyieldmaintenanceperiod",
    "Type": "bigint"
  },
  {
    "Name": "yieldmaintenanceendperiod",
    "Type": "bigint"
  },
  {
    "Name": "ymclimit",
    "Type": "double"
  },
  {
    "Name": "ymclimittype",
    "Type": "string"
  },
  {
    "Name": "ymcspread",
    "Type": "double"
  },
  {
    "Name": "firstpremiumperiod",
    "Type": "bigint"
  },
  {
    "Name": "prepaymentpremiumendperiod",
    "Type": "bigint"
  },
  {
    "Name": "prepaymenttermsdescription",
    "Type": "string"
  },
  {
    "Name": "armindexcode",
    "Type": "string"
  },
  {
    "Name": "armmargin",
    "Type": "double"
  },
  {
    "Name": "lifetimeratecap",
    "Type": "double"
  },
  {
    "Name": "lifetimeratefloor",
    "Type": "double"
  },
  {
    "Name": "periodicrateincreaselimit",
    "Type": "double"
  },
  {
    "Name": "periodicratedecreaselimit",
    "Type": "double"
  },
  {
    "Name": "periodicpaymentadjmaxpercentage",
    "Type": "double"
  },
  {
    "Name": "periodicpaymentadjmaxamount",
    "Type": "string"
  },
  {
    "Name": "paymentfrequency",
    "Type": "bigint"
  },
  {
    "Name": "rateresetfrequency_months",
    "Type": "bigint"
  },
  {
    "Name": "paymentresetfrequency_months",
    "Type": "bigint"
  },
  {
    "Name": "monthstonextratereset",
    "Type": "bigint"
  },
  {
    "Name": "monthstonextpaymentreset",
    "Type": "bigint"
  },
  {
    "Name": "recourse_yn",
    "Type": "string"
  },
  {
    "Name": "cross_collaterizedloangrouping",
    "Type": "bigint"
  },
  {
    "Name": "monthsdelinquent",
    "Type": "bigint"
  },
  {
    "Name": "maturitytype",
    "Type": "string"
  },
  {
    "Name": "borrower",
    "Type": "string"
  },
  {
    "Name": "hotelfranchise",
    "Type": "string"
  },
  {
    "Name": "securitytype",
    "Type": "string"
  },
  {
    "Name": "otherinterestadjustment",
    "Type": "double"
  },
  {
    "Name": "cumulativeaccruedunpaidadvanceinterest",
    "Type": "double"
  },
  {
    "Name": "totalreservebalance",
    "Type": "double"
  },
  {
    "Name": "dateaddedtoservicerwatchlist",
    "Type": "date"
  },
  {
    "Name": "specialservicingfeeamountplusadjustments",
    "Type": "double"
  },
  {
    "Name": "reimbursedinterestonadvances",
    "Type": "double"
  },
  {
    "Name": "workoutfeeamount",
    "Type": "double"
  },
  {
    "Name": "liquidationfeeamount",
    "Type": "double"
  },
  {
    "Name": "nonrecoverabilitydetermined",
    "Type": "string"
  },
  {
    "Name": "calculatedmaturitydate",
    "Type": "date"
  },
  {
    "Name": "largesttenant_current",
    "Type": "string"
  },
  {
    "Name": "squarefeetoflargesttenant_current",
    "Type": "double"
  },
  {
    "Name": "secondlargesttenant_current",
    "Type": "string"
  },
  {
    "Name": "squarefeetofsecond_2ndlargesttenant_current",
    "Type": "double"
  },
  {
    "Name": "thirdlargesttenant_current",
    "Type": "string"
  },
  {
    "Name": "squarefeetofthird_3rdlargesttenant_current",
    "Type": "double"
  },
  {
    "Name": "dateofleaseexpirationoflargesttenant_current",
    "Type": "date"
  },
  {
    "Name": "dateofleaseexpirationofsecond_2ndlargesttenant_current",
    "Type": "date"
  },
  {
    "Name": "dateofleaseexpirationofthird_3rdlargesttenant_current",
    "Type": "date"
  },
  {
    "Name": "largesttenantpercent_current",
    "Type": "double"
  },
  {
    "Name": "largesttenantpercent_current2",
    "Type": "double"
  },
  {
    "Name": "largesttenantpercent_current3",
    "Type": "double"
  },
  {
    "Name": "notenumber",
    "Type": "double"
  },
  {
    "Name": "poolnum",
    "Type": "string"
  },
  {
    "Name": "deriveddelinquencystatuscode",
    "Type": "string"
  },
  {
    "Name": "paidoffamount",
    "Type": "double"
  },
  {
    "Name": "dispositiondate",
    "Type": "date"
  },
  {
    "Name": "lastpaidthrudate",
    "Type": "date"
  },
  {
    "Name": "monthstorecover",
    "Type": "bigint"
  },
  {
    "Name": "prepaymentpenalty",
    "Type": "double"
  },
  {
    "Name": "lossamount",
    "Type": "double"
  },
  {
    "Name": "calculatedlosspercent",
    "Type": "double"
  },
  {
    "Name": "dispositiontype",
    "Type": "string"
  },
  {
    "Name": "dispositionsubtype",
    "Type": "string"
  },
  {
    "Name": "dispositioncomments",
    "Type": "string"
  },
  {
    "Name": "prepaymentexposureamount",
    "Type": "double"
  },
  {
    "Name": "prepaymentexposurepercent",
    "Type": "double"
  },
  {
    "Name": "acrossdealsloanidtrepp",
    "Type": "string"
  },
  {
    "Name": "notepercentpledged",
    "Type": "double"
  },
  {
    "Name": "loaninotherdeals",
    "Type": "string"
  },
  {
    "Name": "currentwholeloanendingbalance",
    "Type": "double"
  },
  {
    "Name": "liquidationsalesprice",
    "Type": "double"
  },
  {
    "Name": "amountsdueservicersandtrustee",
    "Type": "double"
  },
  {
    "Name": "amountsheldbackforfuturepayment",
    "Type": "double"
  },
  {
    "Name": "accruedinterest",
    "Type": "double"
  },
  {
    "Name": "additionaltrustfundexpense",
    "Type": "double"
  },
  {
    "Name": "currentperiodadjustmenttoloan_principal",
    "Type": "double"
  },
  {
    "Name": "dateofcurrentperiodadjustmenttoloan",
    "Type": "date"
  },
  {
    "Name": "cumulativeadjustmentstoloan",
    "Type": "double"
  },
  {
    "Name": "advancedbytrustnonrecoverablereimbursementstoservicer_currentmonth",
    "Type": "double"
  },
  {
    "Name": "anticipatedamounttobeadvancedbytrust_lefttoreimburseservicer",
    "Type": "double"
  },
  {
    "Name": "other_shortfallsrefunds",
    "Type": "double"
  },
  {
    "Name": "numberofnotes",
    "Type": "bigint"
  },
  {
    "Name": "ardflag",
    "Type": "string"
  },
  {
    "Name": "gurantor",
    "Type": "string"
  },
  {
    "Name": "country",
    "Type": "string"
  },
  {
    "Name": "multifamilydirected",
    "Type": "string"
  },
  {
    "Name": "delinquencystatushistory",
    "Type": "string"
  },
  {
    "Name": "delinquencycount",
    "Type": "bigint"
  },
  {
    "Name": "currentmonthlockout",
    "Type": "bigint"
  },
  {
    "Name": "currentmonthymc",
    "Type": "bigint"
  },
  {
    "Name": "currentmonthprepaymentpremium",
    "Type": "bigint"
  },
  {
    "Name": "securitizedmonthlockout",
    "Type": "bigint"
  },
  {
    "Name": "securitizedmonthymc",
    "Type": "bigint"
  },
  {
    "Name": "securitizedmonthprepaymentpremium",
    "Type": "bigint"
  },
  {
    "Name": "currentprepaymentrestriction",
    "Type": "string"
  },
  {
    "Name": "firstcallperiod",
    "Type": "bigint"
  },
  {
    "Name": "periodspastmaturity",
    "Type": "bigint"
  },
  {
    "Name": "derivedicr_noi",
    "Type": "string"
  },
  {
    "Name": "derivedicr_noicode",
    "Type": "string"
  },
  {
    "Name": "derivedicr_ncf",
    "Type": "string"
  },
  {
    "Name": "derivedicr_ncfcode",
    "Type": "string"
  },
  {
    "Name": "renovationyearatsecuritization",
    "Type": "bigint"
  },
  {
    "Name": "securitizedpayment",
    "Type": "double"
  },
  {
    "Name": "loanpurpose",
    "Type": "string"
  },
  {
    "Name": "extensiontype",
    "Type": "string"
  },
  {
    "Name": "l_specialservicer",
    "Type": "string"
  },
  {
    "Name": "modificationdate_trepp",
    "Type": "date"
  },
  {
    "Name": "derivedloanmodificationstatus",
    "Type": "string"
  },
  {
    "Name": "modificationdescription_trepp",
    "Type": "string"
  },
  {
    "Name": "modifiedloandescription",
    "Type": "string"
  },
  {
    "Name": "modifiedloansubordinationlevel_trepp",
    "Type": "string"
  },
  {
    "Name": "modifiedhopenoteflag",
    "Type": "string"
  },
  {
    "Name": "modifiedloanprincipalforgiveness_trepp",
    "Type": "string"
  },
  {
    "Name": "modifiedrate_trepp",
    "Type": "double"
  },
  {
    "Name": "modifiedinterestonlyperiodchange",
    "Type": "bigint"
  },
  {
    "Name": "modifiedoriginaltermchange",
    "Type": "bigint"
  },
  {
    "Name": "splitloanreason",
    "Type": "string"
  },
  {
    "Name": "splitloandates",
    "Type": "string"
  },
  {
    "Name": "splitloanidentifier",
    "Type": "bigint"
  },
  {
    "Name": "newlydelinquent",
    "Type": "string"
  },
  {
    "Name": "newlysenttospecialservicing",
    "Type": "string"
  },
  {
    "Name": "newlyonwatchlist",
    "Type": "string"
  },
  {
    "Name": "derivedsecuritizeddebtyieldnoi",
    "Type": "double"
  },
  {
    "Name": "derivedcurrentdebtyieldnoi",
    "Type": "double"
  },
  {
    "Name": "derivedsecuritizeddebtyieldncf",
    "Type": "double"
  },
  {
    "Name": "derivedcurrentdebtyieldncf",
    "Type": "double"
  },
  {
    "Name": "seasoning",
    "Type": "bigint"
  },
  {
    "Name": "amortizationtype",
    "Type": "string"
  },
  {
    "Name": "region",
    "Type": "string"
  },
  {
    "Name": "mortgageloanseller",
    "Type": "string"
  },
  {
    "Name": "affiliatedsponsors",
    "Type": "string"
  },
  {
    "Name": "loantype",
    "Type": "string"
  },
  {
    "Name": "securitizationparipassudebt_anote",
    "Type": "double"
  },
  {
    "Name": "securitizationtotaltrustbalance",
    "Type": "string"
  },
  {
    "Name": "securitizationmasterservicer",
    "Type": "string"
  },
  {
    "Name": "securitizationspecialservicer",
    "Type": "string"
  },
  {
    "Name": "singletenantflag",
    "Type": "string"
  },
  {
    "Name": "fourthlargesttenant",
    "Type": "string"
  },
  {
    "Name": "fourthlargesttenantsquarefootage",
    "Type": "double"
  },
  {
    "Name": "fourthlargesttenantpercent",
    "Type": "double"
  },
  {
    "Name": "fourthlargesttenantleaseexpirationdate",
    "Type": "date"
  },
  {
    "Name": "fifthlargesttenant",
    "Type": "string"
  },
  {
    "Name": "fifthlargesttenantsquarefootage",
    "Type": "double"
  },
  {
    "Name": "fifthlargesttenantpercent",
    "Type": "double"
  },
  {
    "Name": "fifthlargesttenantleaseexpirationdate",
    "Type": "date"
  },
  {
    "Name": "totalexposure",
    "Type": "double"
  },
  {
    "Name": "fourthlargesttenant_current",
    "Type": "string"
  },
  {
    "Name": "squarefeetoffourth_4thlargesttenant_current",
    "Type": "double"
  },
  {
    "Name": "largestcurrenttenantpercent4",
    "Type": "double"
  },
  {
    "Name": "dateofleaseexpirationoffourth_4thlargesttenant_current",
    "Type": "date"
  },
  {
    "Name": "fifthlargesttenant_current",
    "Type": "string"
  },
  {
    "Name": "squarefeetoffifth_5thlargesttenant_current",
    "Type": "double"
  },
  {
    "Name": "largestcurrenttenantpercent5",
    "Type": "double"
  },
  {
    "Name": "dateofleaseexpirationoffifth_5thlargesttenant_current",
    "Type": "date"
  },
  {
    "Name": "modifiedborrowersequity_trepp",
    "Type": "string"
  },
  {
    "Name": "modifiedrate2_trepp",
    "Type": "string"
  },
  {
    "Name": "modificationdate2_trepp",
    "Type": "string"
  },
  {
    "Name": "modificationdescription2_trepp",
    "Type": "string"
  },
  {
    "Name": "modifiedloan2subordinationlevel_trepp",
    "Type": "string"
  },
  {
    "Name": "modified2loanprincipalforgiveness_trepp",
    "Type": "string"
  },
  {
    "Name": "fullmodification2notmodeledduetounavailableinfo",
    "Type": "string"
  },
  {
    "Name": "modified2borrowersequity_trepp",
    "Type": "string"
  },
  {
    "Name": "reasonforspecialservicertransfer",
    "Type": "string"
  },
  {
    "Name": "advancedbytrust_cumulative",
    "Type": "double"
  },
  {
    "Name": "modificationbookingdate",
    "Type": "string"
  },
  {
    "Name": "modificationexecutiondate",
    "Type": "date"
  },
  {
    "Name": "currentperiodadjustmenttoloan_other",
    "Type": "double"
  },
  {
    "Name": "seismiczoneflag",
    "Type": "string"
  },
  {
    "Name": "masterservicer",
    "Type": "string"
  },
  {
    "Name": "curloanspecialservicer",
    "Type": "string"
  },
  {
    "Name": "derivedltv2",
    "Type": "double"
  },
  {
    "Name": "cumulativewodra",
    "Type": "string"
  },
  {
    "Name": "currentnetrentablesquarefeet",
    "Type": "double"
  },
  {
    "Name": "currentbalancepersqftorunit",
    "Type": "string"
  },
  {
    "Name": "currentnumberofunitsbedsrooms",
    "Type": "bigint"
  },
  {
    "Name": "firstopendate",
    "Type": "date"
  },
  {
    "Name": "treppderivedmsaranking",
    "Type": "bigint"
  },
  {
    "Name": "nameoftranchespaidbythisloan",
    "Type": "string"
  },
  {
    "Name": "pctsqfeetexpiring1_12months",
    "Type": "double"
  },
  {
    "Name": "pctsqfeetexpiring13_24months",
    "Type": "double"
  },
  {
    "Name": "pctsqfeetexpiring25_36months",
    "Type": "double"
  },
  {
    "Name": "pctsqfeetexpiring37_48months",
    "Type": "double"
  },
  {
    "Name": "pctsqfeetexpiring49_months",
    "Type": "double"
  },
  {
    "Name": "derivednoincf",
    "Type": "double"
  },
  {
    "Name": "derivednoincfcode",
    "Type": "string"
  },
  {
    "Name": "loanpiecesexistflag",
    "Type": "string"
  },
  {
    "Name": "remainingperiodsuntilfirstdefeasible",
    "Type": "bigint"
  },
  {
    "Name": "modificationindicator",
    "Type": "bigint"
  },
  {
    "Name": "cumulativenonrecoverableinterest",
    "Type": "double"
  },
  {
    "Name": "leadtransactionid",
    "Type": "string"
  },
  {
    "Name": "advancedbytrust_workoutdelayedreimbursementamounts_wodratoservicer_currentmonth",
    "Type": "string"
  },
  {
    "Name": "disclosablespecialservicingfees",
    "Type": "string"
  },
  {
    "Name": "loandefault",
    "Type": "int"
  },
  {
    "Name": "filedate",
    "Type": "date"
  },
  {
    "Name": "month",
    "Type": "int"
  },
  {
    "Name": "dealsflag",
    "Type": "string"
  },
  {
    "Name": "compendiumdealflag",
    "Type": "boolean"
  },
  {
    "Name": "compendiumdealname",
    "Type": "string"
  },
  {
    "Name": "creclobloombergname",
    "Type": "string"
  },
  {
    "Name": "normalizedmsanames",
    "Type": "string"
  },
  {
    "Name": "treppdealnameloanid",
    "Type": "string"
  },
  {
    "Name": "bloombergdealnameloanid",
    "Type": "string"
  },
  {
    "Name": "bloombergname",
    "Type": "string"
  },
  {
    "Name": "dealcategory",
    "Type": "string"
  },
  {
    "Name": "isprivateflag",
    "Type": "bigint"
  },
  {
    "Name": "deriveddelinquencystatus",
    "Type": "string"
  },
  {
    "Name": "watchlist",
    "Type": "string"
  },
  {
    "Name": "specialservice",
    "Type": "string"
  },
  {
    "Name": "deliquent",
    "Type": "string"
  },
  {
    "Name": "grace_period_loan",
    "Type": "string"
  },
  {
    "Name": "transidtrustee",
    "Type": "string"
  },
  {
    "Name": "groupidtrustee",
    "Type": "string"
  },
  {
    "Name": "collateralid",
    "Type": "string"
  },
  {
    "Name": "curindexrate",
    "Type": "double"
  },
  {
    "Name": "striprate1",
    "Type": "double"
  },
  {
    "Name": "striprate2",
    "Type": "double"
  },
  {
    "Name": "striprate3",
    "Type": "double"
  },
  {
    "Name": "striprate4",
    "Type": "double"
  },
  {
    "Name": "striprate5",
    "Type": "double"
  },
  {
    "Name": "nextindexrate",
    "Type": "double"
  },
  {
    "Name": "nextrate",
    "Type": "double"
  },
  {
    "Name": "nextratechgdate",
    "Type": "bigint"
  },
  {
    "Name": "nextpmtchgdate",
    "Type": "bigint"
  },
  {
    "Name": "curdeferred",
    "Type": "double"
  },
  {
    "Name": "pppenint",
    "Type": "double"
  },
  {
    "Name": "expresolutiondate",
    "Type": "bigint"
  },
  {
    "Name": "curhyperamortdate",
    "Type": "bigint"
  },
  {
    "Name": "lastsetupchgdate",
    "Type": "bigint"
  },
  {
    "Name": "lastloancontribdate",
    "Type": "bigint"
  },
  {
    "Name": "lastpropcontribdate",
    "Type": "bigint"
  },
  {
    "Name": "assumptiondate",
    "Type": "bigint"
  },
  {
    "Name": "origpmtdate",
    "Type": "bigint"
  },
  {
    "Name": "securaterm",
    "Type": "bigint"
  },
  {
    "Name": "graceper",
    "Type": "bigint"
  },
  {
    "Name": "affiliatedborrowers",
    "Type": "string"
  },
  {
    "Name": "escrowflag",
    "Type": "string"
  },
  {
    "Name": "reserveflag",
    "Type": "string"
  },
  {
    "Name": "hasballoon",
    "Type": "string"
  },
  {
    "Name": "prosploanidtrepp",
    "Type": "string"
  },
  {
    "Name": "prosploanidtrustee",
    "Type": "string"
  },
  {
    "Name": "origloanbaltrustee",
    "Type": "double"
  },
  {
    "Name": "securoterm",
    "Type": "bigint"
  },
  {
    "Name": "legalmaturitydate",
    "Type": "bigint"
  },
  {
    "Name": "extoption1",
    "Type": "bigint"
  },
  {
    "Name": "extoption2",
    "Type": "bigint"
  },
  {
    "Name": "extoption3",
    "Type": "bigint"
  },
  {
    "Name": "extoption4",
    "Type": "string"
  },
  {
    "Name": "extoption5",
    "Type": "string"
  },
  {
    "Name": "mrfytdicrnoi",
    "Type": "string"
  },
  {
    "Name": "mrfytdicrncf",
    "Type": "string"
  },
  {
    "Name": "priorfyicrnoi",
    "Type": "string"
  },
  {
    "Name": "priorfyicrncf",
    "Type": "string"
  },
  {
    "Name": "secpriorfyicrnoi",
    "Type": "string"
  },
  {
    "Name": "secpriorfyicrncf",
    "Type": "string"
  },
  {
    "Name": "curicr",
    "Type": "string"
  },
  {
    "Name": "icrasof",
    "Type": "string"
  },
  {
    "Name": "securicrnoi",
    "Type": "string"
  },
  {
    "Name": "securicrncf",
    "Type": "string"
  },
  {
    "Name": "securicrnoincf",
    "Type": "string"
  },
  {
    "Name": "covenanticrtext",
    "Type": "string"
  },
  {
    "Name": "covenantltvtext",
    "Type": "string"
  },
  {
    "Name": "covenantothertext",
    "Type": "string"
  },
  {
    "Name": "cdoassettype",
    "Type": "string"
  },
  {
    "Name": "currlockboxstatus",
    "Type": "string"
  },
  {
    "Name": "cumdefint",
    "Type": "double"
  },
  {
    "Name": "defintcoll",
    "Type": "double"
  },
  {
    "Name": "secioperiods",
    "Type": "bigint"
  },
  {
    "Name": "secdebtserv",
    "Type": "double"
  },
  {
    "Name": "totremextperiods",
    "Type": "bigint"
  },
  {
    "Name": "loanmodunavailtrepp",
    "Type": "string"
  },
  {
    "Name": "derivedloanstatus",
    "Type": "string"
  },
  {
    "Name": "swapfixedrate",
    "Type": "string"
  },
  {
    "Name": "swapmatdt",
    "Type": "string"
  },
  {
    "Name": "swapnotionalbal",
    "Type": "string"
  },
  {
    "Name": "fhaprogramflag",
    "Type": "string"
  },
  {
    "Name": "hotelflag",
    "Type": "string"
  },
  {
    "Name": "origholdback",
    "Type": "string"
  },
  {
    "Name": "fullyextendedmatdt",
    "Type": "date"
  },
  {
    "Name": "firstpmtdtpandi",
    "Type": "date"
  },
  {
    "Name": "lastiopmtdt",
    "Type": "string"
  },
  {
    "Name": "secamorttype",
    "Type": "string"
  },
  {
    "Name": "secdebtserviceio",
    "Type": "string"
  },
  {
    "Name": "secdebtserviceioallin",
    "Type": "string"
  },
  {
    "Name": "secdebtservicepandiallin",
    "Type": "string"
  },
  {
    "Name": "secdebtyieldnoiallin",
    "Type": "string"
  },
  {
    "Name": "secdebtyieldncfallin",
    "Type": "string"
  },
  {
    "Name": "secdebtyieldnoinew",
    "Type": "double"
  },
  {
    "Name": "secdebtyieldncfnew",
    "Type": "double"
  },
  {
    "Name": "secnoidscramortpi",
    "Type": "string"
  },
  {
    "Name": "secnetcfdscramortpi",
    "Type": "string"
  },
  {
    "Name": "secnoidscrio",
    "Type": "string"
  },
  {
    "Name": "secnetcfdscrio",
    "Type": "string"
  },
  {
    "Name": "secdscramortallin",
    "Type": "string"
  },
  {
    "Name": "secnetcfdscramortallin",
    "Type": "string"
  },
  {
    "Name": "secltvallin",
    "Type": "string"
  },
  {
    "Name": "secmatdtltvallin",
    "Type": "string"
  },
  {
    "Name": "sec3rdmrenddt",
    "Type": "date"
  },
  {
    "Name": "sec3rdmregi",
    "Type": "string"
  },
  {
    "Name": "sec3rdmroperexp",
    "Type": "string"
  },
  {
    "Name": "sec3rdmrnoi",
    "Type": "double"
  },
  {
    "Name": "sec3rdmrcapexp",
    "Type": "double"
  },
  {
    "Name": "sec3rdmrncf",
    "Type": "double"
  },
  {
    "Name": "sec3rdmroccpancypct",
    "Type": "double"
  },
  {
    "Name": "sec3rdmrdebtyieldnoi",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrenddt",
    "Type": "date"
  },
  {
    "Name": "sec2ndmregi",
    "Type": "string"
  },
  {
    "Name": "sec2ndmroperexp",
    "Type": "string"
  },
  {
    "Name": "sec2ndmrnoi",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrcapexp",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrncf",
    "Type": "double"
  },
  {
    "Name": "sec2ndmroccpancypct",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrdebtyieldnoi",
    "Type": "double"
  },
  {
    "Name": "secmrbegdt",
    "Type": "string"
  },
  {
    "Name": "secmrenddt",
    "Type": "date"
  },
  {
    "Name": "secmrdttype",
    "Type": "string"
  },
  {
    "Name": "secmregi",
    "Type": "string"
  },
  {
    "Name": "secmroperexp",
    "Type": "string"
  },
  {
    "Name": "secmrnoi",
    "Type": "double"
  },
  {
    "Name": "secmrcapexp",
    "Type": "double"
  },
  {
    "Name": "secmrncf",
    "Type": "double"
  },
  {
    "Name": "secmroccpancypct",
    "Type": "double"
  },
  {
    "Name": "secmrdebtyieldnoi",
    "Type": "double"
  },
  {
    "Name": "secegi",
    "Type": "double"
  },
  {
    "Name": "secexpensesoper",
    "Type": "string"
  },
  {
    "Name": "secreplaceres",
    "Type": "double"
  },
  {
    "Name": "secexpensescap",
    "Type": "double"
  },
  {
    "Name": "sec3rdmradr",
    "Type": "string"
  },
  {
    "Name": "sec3rdmrrevpar",
    "Type": "string"
  },
  {
    "Name": "sec2ndmradr",
    "Type": "string"
  },
  {
    "Name": "sec2ndmrrevpar",
    "Type": "string"
  },
  {
    "Name": "secmradr",
    "Type": "string"
  },
  {
    "Name": "secmrrevpar",
    "Type": "string"
  },
  {
    "Name": "secadr",
    "Type": "string"
  },
  {
    "Name": "secrevpar",
    "Type": "string"
  },
  {
    "Name": "sectaxescupfront",
    "Type": "double"
  },
  {
    "Name": "sectaxescmonthly",
    "Type": "double"
  },
  {
    "Name": "sectaxesccashorloc",
    "Type": "string"
  },
  {
    "Name": "sectaxescloccntpty",
    "Type": "string"
  },
  {
    "Name": "secinsescupfront",
    "Type": "double"
  },
  {
    "Name": "secinsescmonthly",
    "Type": "double"
  },
  {
    "Name": "secinsesccashorloc",
    "Type": "string"
  },
  {
    "Name": "secinsescloccntpty",
    "Type": "string"
  },
  {
    "Name": "secreplaceresupfront",
    "Type": "double"
  },
  {
    "Name": "secreplaceresmonthly",
    "Type": "double"
  },
  {
    "Name": "secreplacerescap",
    "Type": "string"
  },
  {
    "Name": "secreplacerescashorloc",
    "Type": "string"
  },
  {
    "Name": "secrepresescloccntpty",
    "Type": "string"
  },
  {
    "Name": "sectilcresupfront",
    "Type": "double"
  },
  {
    "Name": "sectilcresmonthly",
    "Type": "double"
  },
  {
    "Name": "sectilcrescap",
    "Type": "double"
  },
  {
    "Name": "sectilcrescashorloc",
    "Type": "string"
  },
  {
    "Name": "sectilcresloccntpty",
    "Type": "string"
  },
  {
    "Name": "secdebtsvcresupfront",
    "Type": "string"
  },
  {
    "Name": "secdebtsvcresmonthly",
    "Type": "string"
  },
  {
    "Name": "secdebtsvcrescap",
    "Type": "string"
  },
  {
    "Name": "secdebtsvcrescashorloc",
    "Type": "string"
  },
  {
    "Name": "secotherres1type",
    "Type": "string"
  },
  {
    "Name": "secotherres1upfront",
    "Type": "string"
  },
  {
    "Name": "secotherres1monthly",
    "Type": "string"
  },
  {
    "Name": "secotherres1cap",
    "Type": "string"
  },
  {
    "Name": "secotherres1cashorloc",
    "Type": "string"
  },
  {
    "Name": "secotherres1loccntpty",
    "Type": "string"
  },
  {
    "Name": "secotherres2type",
    "Type": "string"
  },
  {
    "Name": "secotherres2upfront",
    "Type": "string"
  },
  {
    "Name": "secotherres2monthly",
    "Type": "string"
  },
  {
    "Name": "secotherres2cap",
    "Type": "string"
  },
  {
    "Name": "secotherres2cashorloc",
    "Type": "string"
  },
  {
    "Name": "secotherres2loccntpty",
    "Type": "string"
  },
  {
    "Name": "secotherres3type",
    "Type": "string"
  },
  {
    "Name": "secotherres3upfront",
    "Type": "string"
  },
  {
    "Name": "secotherres3monthly",
    "Type": "string"
  },
  {
    "Name": "secotherres3cap",
    "Type": "string"
  },
  {
    "Name": "secotherres3cashorloc",
    "Type": "string"
  },
  {
    "Name": "secotherres3loccntpty",
    "Type": "string"
  },
  {
    "Name": "secotherres4type",
    "Type": "string"
  },
  {
    "Name": "secotherres4upfront",
    "Type": "string"
  },
  {
    "Name": "secotherres4monthly",
    "Type": "string"
  },
  {
    "Name": "secotherres4cap",
    "Type": "string"
  },
  {
    "Name": "secotherres4cashorloc",
    "Type": "string"
  },
  {
    "Name": "secotherres4loccntpty",
    "Type": "string"
  },
  {
    "Name": "secotherres5type",
    "Type": "string"
  },
  {
    "Name": "secotherres5upfront",
    "Type": "string"
  },
  {
    "Name": "secotherres5monthly",
    "Type": "string"
  },
  {
    "Name": "secotherres5cap",
    "Type": "string"
  },
  {
    "Name": "secotherres5cashorloc",
    "Type": "string"
  },
  {
    "Name": "secotherres5loccntpty",
    "Type": "string"
  },
  {
    "Name": "secotherres6type",
    "Type": "string"
  },
  {
    "Name": "secotherres6upfront",
    "Type": "string"
  },
  {
    "Name": "secotherres6monthly",
    "Type": "string"
  },
  {
    "Name": "secotherres6cap",
    "Type": "string"
  },
  {
    "Name": "secotherres6cashorloc",
    "Type": "string"
  },
  {
    "Name": "secotherres6loccntpty",
    "Type": "string"
  },
  {
    "Name": "seclockboxflag",
    "Type": "string"
  },
  {
    "Name": "seclockboxtype",
    "Type": "string"
  },
  {
    "Name": "secadditionalcfpledge",
    "Type": "string"
  },
  {
    "Name": "seclatestfyeactualcfamt",
    "Type": "string"
  },
  {
    "Name": "secannualcfamount",
    "Type": "string"
  },
  {
    "Name": "seclockbox",
    "Type": "string"
  },
  {
    "Name": "sectilcres",
    "Type": "double"
  },
  {
    "Name": "sec3rdmrrevenues",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrrevenues",
    "Type": "double"
  },
  {
    "Name": "secmrrevenues",
    "Type": "double"
  },
  {
    "Name": "sec3rdmrexp",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrexp",
    "Type": "double"
  },
  {
    "Name": "secmrexp",
    "Type": "double"
  },
  {
    "Name": "exposure1",
    "Type": "double"
  },
  {
    "Name": "exposure2",
    "Type": "double"
  },
  {
    "Name": "exposure3",
    "Type": "double"
  },
  {
    "Name": "exposure4",
    "Type": "double"
  },
  {
    "Name": "exposure5",
    "Type": "double"
  },
  {
    "Name": "secdefmaintresupfront",
    "Type": "double"
  },
  {
    "Name": "secenvironmentalresupfront",
    "Type": "string"
  },
  {
    "Name": "noncashprincipaladjustment",
    "Type": "double"
  },
  {
    "Name": "loantovalue2typecd",
    "Type": "bigint"
  },
  {
    "Name": "currentablearea",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrdatetype",
    "Type": "string"
  },
  {
    "Name": "sec3rdmrdatetype",
    "Type": "string"
  },
  {
    "Name": "loanmodifiedderivednumber",
    "Type": "bigint"
  },
  {
    "Name": "apprvalueltvpct",
    "Type": "string"
  },
  {
    "Name": "reportingperiodbegindt",
    "Type": "date"
  },
  {
    "Name": "reportingperiodenddt",
    "Type": "date"
  },
  {
    "Name": "demandresolutiondt",
    "Type": "date"
  },
  {
    "Name": "assetsubjecttodemandflag",
    "Type": "bigint"
  },
  {
    "Name": "assetsubjecttodemandstatus",
    "Type": "bigint"
  },
  {
    "Name": "repurchasereplacereason",
    "Type": "string"
  },
  {
    "Name": "postmodificationamortizationperiod",
    "Type": "string"
  },
  {
    "Name": "curnonrecoverableinterest",
    "Type": "double"
  },
  {
    "Name": "cumulativeardinterest",
    "Type": "double"
  },
  {
    "Name": "ardinterestcollected",
    "Type": "double"
  },
  {
    "Name": "repurchaseamt",
    "Type": "string"
  },
  {
    "Name": "excessliquidationproceeds",
    "Type": "string"
  },
  {
    "Name": "secpurchaseprice",
    "Type": "string"
  },
  {
    "Name": "secclosingcosts",
    "Type": "string"
  },
  {
    "Name": "totseccostbasispostrehab",
    "Type": "string"
  },
  {
    "Name": "secannualcontractualrent",
    "Type": "string"
  },
  {
    "Name": "rentedflag",
    "Type": "bigint"
  },
  {
    "Name": "origleaseterm",
    "Type": "string"
  },
  {
    "Name": "totseccostbasisprerehab",
    "Type": "string"
  },
  {
    "Name": "lifeindexcapborrower",
    "Type": "string"
  },
  {
    "Name": "defeasstatusraw",
    "Type": "string"
  },
  {
    "Name": "correctedstatus",
    "Type": "string"
  },
  {
    "Name": "defeasancetomaturityflag",
    "Type": "string"
  },
  {
    "Name": "curcrosscollateralizationnum",
    "Type": "string"
  },
  {
    "Name": "agencyid",
    "Type": "string"
  },
  {
    "Name": "cursecuritytype",
    "Type": "string"
  },
  {
    "Name": "resecuritizedflag",
    "Type": "string"
  },
  {
    "Name": "paripassusecbal",
    "Type": "double"
  },
  {
    "Name": "paripassupct",
    "Type": "double"
  },
  {
    "Name": "secleadmasterservicer",
    "Type": "string"
  },
  {
    "Name": "secleadspecialservicer",
    "Type": "string"
  },
  {
    "Name": "seccontrollingnoteholder",
    "Type": "string"
  },
  {
    "Name": "covenantdebtyield",
    "Type": "string"
  },
  {
    "Name": "secappraiser",
    "Type": "string"
  },
  {
    "Name": "engineeringrptdt",
    "Type": "bigint"
  },
  {
    "Name": "environmentalphase1rptdt",
    "Type": "date"
  },
  {
    "Name": "environmentalphase2rptdt",
    "Type": "date"
  },
  {
    "Name": "seismicrptdt",
    "Type": "date"
  },
  {
    "Name": "seismicpmlpct",
    "Type": "double"
  },
  {
    "Name": "terrorisminsuranceflag",
    "Type": "string"
  },
  {
    "Name": "earthquakeinsuranceflag",
    "Type": "string"
  },
  {
    "Name": "environmentalphase2flag",
    "Type": "string"
  },
  {
    "Name": "environmentalinsuranceflag",
    "Type": "string"
  },
  {
    "Name": "speflag",
    "Type": "string"
  },
  {
    "Name": "greenprogram",
    "Type": "string"
  },
  {
    "Name": "greencertifications",
    "Type": "string"
  },
  {
    "Name": "lowincomeunits",
    "Type": "string"
  },
  {
    "Name": "verylowincomeunits",
    "Type": "string"
  },
  {
    "Name": "rentalsubsidyindicatorflag",
    "Type": "string"
  },
  {
    "Name": "rentalsubsidytype",
    "Type": "string"
  },
  {
    "Name": "secterminationoptionflag1",
    "Type": "string"
  },
  {
    "Name": "secterminationoptionflag2",
    "Type": "string"
  },
  {
    "Name": "secterminationoptionflag3",
    "Type": "string"
  },
  {
    "Name": "secterminationoptionflag4",
    "Type": "string"
  },
  {
    "Name": "secterminationoptionflag5",
    "Type": "string"
  },
  {
    "Name": "secearlyleaseterminationdt1",
    "Type": "string"
  },
  {
    "Name": "secearlyleaseterminationdt2",
    "Type": "string"
  },
  {
    "Name": "secearlyleaseterminationdt3",
    "Type": "string"
  },
  {
    "Name": "secearlyleaseterminationdt4",
    "Type": "string"
  },
  {
    "Name": "secearlyleaseterminationdt5",
    "Type": "string"
  },
  {
    "Name": "balloonltvtotalmortgage",
    "Type": "string"
  },
  {
    "Name": "sectotalmortgagedscrnoi",
    "Type": "string"
  },
  {
    "Name": "sectotalmortgagedscrncf",
    "Type": "string"
  },
  {
    "Name": "sectotalmortgagedebtyieldnoi",
    "Type": "string"
  },
  {
    "Name": "sectotalmortgagedebtyieldncf",
    "Type": "string"
  },
  {
    "Name": "sectotalmortgageltv",
    "Type": "string"
  },
  {
    "Name": "sectotalmortgagedebtserviceio",
    "Type": "string"
  },
  {
    "Name": "sectotalmortgagedebtservice",
    "Type": "string"
  },
  {
    "Name": "secjuniorbalance",
    "Type": "double"
  },
  {
    "Name": "secmezzbalance",
    "Type": "string"
  },
  {
    "Name": "secappraisedvalueasis",
    "Type": "double"
  },
  {
    "Name": "secappraisalasisdt",
    "Type": "date"
  },
  {
    "Name": "secltvasis",
    "Type": "double"
  },
  {
    "Name": "secoccupancyrateasis",
    "Type": "double"
  },
  {
    "Name": "secrevenuesasis",
    "Type": "double"
  },
  {
    "Name": "secexpensesasis",
    "Type": "double"
  },
  {
    "Name": "secnoiasis",
    "Type": "double"
  },
  {
    "Name": "secreplacementreserveasis",
    "Type": "double"
  },
  {
    "Name": "secncfasis",
    "Type": "double"
  },
  {
    "Name": "secdscrnoiasis",
    "Type": "double"
  },
  {
    "Name": "secdscrncfasis",
    "Type": "double"
  },
  {
    "Name": "secdebtyieldnoiasis",
    "Type": "double"
  },
  {
    "Name": "secdebtyieldncfasis",
    "Type": "double"
  },
  {
    "Name": "secmrdscrnoi",
    "Type": "double"
  },
  {
    "Name": "secmrdscrncf",
    "Type": "double"
  },
  {
    "Name": "secmrdebtyieldncf",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrdscrnoi",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrdscrncf",
    "Type": "double"
  },
  {
    "Name": "sec2ndmrdebtyieldncf",
    "Type": "string"
  },
  {
    "Name": "sec3rdmrdscrnoi",
    "Type": "double"
  },
  {
    "Name": "sec3rdmrdscrncf",
    "Type": "double"
  },
  {
    "Name": "sec3rdmrdebtyieldncf",
    "Type": "string"
  },
  {
    "Name": "secdebtsvcescloccntpty",
    "Type": "string"
  },
  {
    "Name": "covenantdscrtext",
    "Type": "string"
  },
  {
    "Name": "year",
    "Type": "string",
    "PartitionKey": "Partition (0)"
  }
]

def validate_comments(expected, actual):
    errors = []

    # Convert actual schema into a lookup dict
    actual_comments = {
        field["Name"]: field.get("Comment", "")
        for field in actual
    }

    # Check for missing or mismatched comments
    for name, expected_comment in expected.items():
        if name not in actual_comments:
            errors.append(f"Missing field: {name}")
        elif actual_comments[name] != expected_comment:
            errors.append(
                f"Comment mismatch for '{name}': "
                f"expected '{expected_comment}', "
                f"found '{actual_comments[name]}'"
            )

    # Check for unexpected extra fields
    for name in actual_comments:
        if name not in expected:
            errors.append(f"Unexpected field present: {name}")

    return errors


# Run validation
validation_errors = validate_comments(expected_comments, actual_schema)

if not validation_errors:
    print("All comments match exactly.")
else:
    print("Validation errors found:")
    for err in validation_errors:
        print(f" - {err}")
