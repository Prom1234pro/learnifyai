from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Affiliate, Referrals, Commission, ReferralStatus, CommissionStatus
from main.authentication.models import User
from main.utils import admin_required

affiliate_bp = Blueprint('affiliate', __name__)

# Manage affiliates
@affiliate_bp.route('/affiliates', methods=['GET', 'POST'])
@admin_required
def manage_affiliates():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            commission_rate = request.form['commission_rate']
            affiliate_token = request.form['affiliate_token']

            new_affiliate = Affiliate(user_id=user_id, commission_rate=commission_rate, affiliate_token=affiliate_token)
            db.session.add(new_affiliate)
            db.session.commit()
            flash('Affiliate added successfully!')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding affiliate: {e}', 'error')
        return redirect(url_for('affiliate.manage_affiliates'))

    affiliates = Affiliate.query.all()
    users = User.query.all()
    return render_template('affiliate/affiliates.html', affiliates=affiliates, users=users)

@affiliate_bp.route('/affiliate/update/<affiliate_id>', methods=['GET', 'POST'])
@admin_required
def update_affiliate(affiliate_id):
    affiliate = Affiliate.query.get_or_404(affiliate_id)
    if request.method == 'POST':
        try:
            affiliate.user_id = request.form['user_id']
            affiliate.commission_rate = request.form['commission_rate']
            affiliate.affiliate_token = request.form['affiliate_token']

            db.session.commit()
            flash('Affiliate updated successfully!')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating affiliate: {e}', 'error')
        return redirect(url_for('affiliate.manage_affiliates'))

    users = User.query.all()
    return render_template('affiliate/update_affiliate.html', affiliate=affiliate, users=users)

@affiliate_bp.route('/affiliate/delete/<affiliate_id>', methods=['POST'])
@admin_required
def delete_affiliate(affiliate_id):
    affiliate = Affiliate.query.get_or_404(affiliate_id)
    try:
        db.session.delete(affiliate)
        db.session.commit()
        flash('Affiliate deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting affiliate: {e}', 'error')
    return redirect(url_for('affiliate.manage_affiliates'))

# Manage referrals
@affiliate_bp.route('/referrals', methods=['GET', 'POST'])
@admin_required
def manage_referrals():
    if request.method == 'POST':
        try:
            affiliate_id = request.form['affiliate_id']
            user_id = request.form['user_id']
            status = request.form['status']

            new_referral = Referrals(affiliate_id=affiliate_id, user_id=user_id, status=status)
            db.session.add(new_referral)
            db.session.commit()
            flash('Referral added successfully!')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding referral: {e}', 'error')
        return redirect(url_for('affiliate.manage_referrals'))

    referrals = Referrals.query.all()
    affiliates = Affiliate.query.all()
    users = User.query.all()
    return render_template('affiliate/referrals.html', referrals=referrals, affiliates=affiliates, users=users)

@affiliate_bp.route('/referral/update/<referral_id>', methods=['POST'])
@admin_required
def update_referral(referral_id):
    referral = Referrals.query.get_or_404(referral_id)
    try:
        referral.status = request.form['status']
        db.session.commit()
        flash('Referral updated successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating referral: {e}', 'error')
    return redirect(url_for('affiliate.manage_referrals'))

@affiliate_bp.route('/referral/delete/<referral_id>', methods=['POST'])
@admin_required
def delete_referral(referral_id):
    referral = Referrals.query.get_or_404(referral_id)
    try:
        db.session.delete(referral)
        db.session.commit()
        flash('Referral deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting referral: {e}', 'error')
    return redirect(url_for('affiliate.manage_referrals'))

# Manage commissions
@affiliate_bp.route('/commissions', methods=['GET', 'POST'])
@admin_required
def manage_commissions():
    if request.method == 'POST':
        try:
            affiliate_id = request.form['affiliate_id']
            amount = request.form['amount']
            status = request.form['status']

            new_commission = Commission(affiliate_id=affiliate_id, amount=amount, status=status)
            db.session.add(new_commission)
            db.session.commit()
            flash('Commission added successfully!')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding commission: {e}', 'error')
        return redirect(url_for('affiliate.manage_commissions'))

    commissions = Commission.query.all()
    affiliates = Affiliate.query.all()
    return render_template('affiliate/commissions.html', commissions=commissions, affiliates=affiliates)

@affiliate_bp.route('/commission/update/<commission_id>', methods=['POST'])
@admin_required
def update_commission(commission_id):
    commission = Commission.query.get_or_404(commission_id)
    try:
        commission.status = request.form['status']
        db.session.commit()
        flash('Commission updated successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating commission: {e}', 'error')
    return redirect(url_for('affiliate.manage_commissions'))

@affiliate_bp.route('/commission/delete/<commission_id>', methods=['POST'])
@admin_required
def delete_commission(commission_id):
    commission = Commission.query.get_or_404(commission_id)
    try:
        db.session.delete(commission)
        db.session.commit()
        flash('Commission deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting commission: {e}', 'error')
    return redirect(url_for('affiliate.manage_commissions'))
